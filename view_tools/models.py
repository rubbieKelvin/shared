## Creates view from models
import typing

from pydantic import BaseModel
from django.db.models import Q, QuerySet

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from shared.utils.query import makeQuery
from shared.abstractmodel import AbstractModel

from .paths import Api
from .body_tools import validate_request
from .pagination import paginate_by_queryparam, paginate
from .exceptions import ResourceNotFound, AccessPermissionError, ApiException


MODEL_VIEW_ACTIONS = typing.Literal[
    "ALL",
    "GET",
    "FIND",
    "INSERT",
    "INSERT_MANY",
    "UPDATE_ONE",
    "UPDATE_MANY",
    "DELETE",
    "DELETE_MANY",
]


class PkSchema(BaseModel):
    pk: int | str


class PksSchema(BaseModel):
    pks: list[int | str]


class FindManySchema(BaseModel):
    where: dict[str, typing.Any]
    limit: int = 100
    offset: int = 0


class InsertManySchema[T: BaseModel](BaseModel):
    objects: list[T]


class UpdateOneSchema[T: BaseModel](PkSchema):
    set_: T


class UpdateManySchema[T: BaseModel](PksSchema):
    set_: T


class PermissionMixin:
    @classmethod
    def permit_get(cls, request: Request):
        raise AccessPermissionError("You're not permitted to access this resource")

    @classmethod
    def permit_insert(cls, request: Request):
        raise AccessPermissionError(
            "You're not permitted to create a resource in this scope"
        )

    @classmethod
    def permit_update(cls, request: Request):
        raise AccessPermissionError("You're not permitted to update a resource")

    @classmethod
    def permit_delete(cls, request: Request):
        raise AccessPermissionError("You're not permitted to delete this resource")


class ModelView[T: AbstractModel](PermissionMixin):
    model: type[T]
    path_root: str | None = None
    base_filter_query: Q | None = None
    must_update_fields: list[str] = [
        "last_updated"
    ]  # fields that must be updated when updating model

    insert_schema: type[BaseModel]
    update_schema: type[UpdateOneSchema]
    update_many_schema: type[UpdateManySchema]
    insert_many_schema: type[InsertManySchema]

    @classmethod
    def fix_pk_type[X: int | str](cls, pk: X) -> X:
        return pk

    @classmethod
    def serializer_func(
        cls, instance: T, scope: MODEL_VIEW_ACTIONS | None = None
    ) -> dict:
        return instance.serialize()

    @typing.final
    @classmethod
    def _get_query_set(cls, request: Request) -> QuerySet[T]:
        # permit
        cls.permit_get(request)
        return (
            cls.model.objects.filter(cls.base_filter_query)
            if cls.base_filter_query
            else cls.model.objects.all()
        )

    @classmethod
    def get(cls, request: Request) -> Response:
        # validate
        body = validate_request(PkSchema, request)

        # get row scope
        query_set = cls._get_query_set(request)

        # get instance
        pk = cls.fix_pk_type(body.pk)

        try:
            instance = query_set.get(pk=pk)
        except cls.model.DoesNotExist:
            raise ResourceNotFound(f"f{cls.model.__class__.__name__}({pk}) not found")

        # return object
        return Response(cls.serializer_func(instance, "GET"))

    @classmethod
    def all(cls, request: Request) -> Response:
        # get row scope
        query_set = cls._get_query_set(request)

        # paginate
        paginated_list = paginate_by_queryparam(request, query_set)

        # response
        return Response([cls.serializer_func(i, "ALL") for i in paginated_list])

    @classmethod
    def find(cls, request: Request) -> Response:
        body = validate_request(FindManySchema, request)
        query = makeQuery(body.where)
        queryset = cls._get_query_set(request).filter(query)

        paginated_list = paginate(queryset, limit=body.limit, offset=body.offset)
        return Response([cls.serializer_func(i, "FIND") for i in paginated_list])

    @classmethod
    def insert(cls, request: Request) -> Response:
        cls.permit_insert(request)
        body = validate_request(cls.insert_schema, request)

        res: T = cls.model.objects.create(**body.model_dump())
        return Response(
            cls.serializer_func(res, "INSERT"), status=status.HTTP_201_CREATED
        )

    @classmethod
    def insert_many(cls, request: Request) -> Response:
        cls.permit_insert(request)
        body = validate_request(cls.insert_many_schema, request)
        instances = [cls.model(**data) for data in body.objects]

        res: list[T] = cls.model.objects.bulk_create(instances)

        return Response(
            [cls.serializer_func(i, "INSERT_MANY") for i in res],
            status=status.HTTP_201_CREATED,
        )

    @classmethod
    def update_one(cls, request: Request) -> Response:
        cls.permit_update(request)
        body = validate_request(cls.update_schema, request)

        pk = cls.fix_pk_type(body.pk)
        queryset = cls._get_query_set(request)
        instance = queryset.get(pk=pk)
        set_ = body.model_dump().get("set_", {})

        for key, value in set_:
            setattr(instance, key, value)

        instance.save()
        return Response(cls.serializer_func(instance, "UPDATE_ONE"))

    @classmethod
    def update_many(cls, request: Request) -> Response:
        cls.permit_update(request)
        query_set = cls._get_query_set(request)
        body = validate_request(cls.update_many_schema, request)
        set_: dict[str, typing.Any] = body.model_dump().get("set_", {})

        instances: list[T] = []

        for pk in body.pks:
            instance = query_set.get(pk=cls.fix_pk_type(pk))

            for key, value in set_.items():
                setattr(instance, key, value)

            instances.append(instance)

        cls.model.objects.bulk_update(
            instances, fields=[*set_.keys(), *cls.must_update_fields]
        )

        return Response([cls.serializer_func(i, "UPDATE_MANY") for i in instances])

    @classmethod
    def delete_one(cls, request: Request) -> Response:
        cls.permit_delete(request)
        query_set = cls._get_query_set(request)
        body = validate_request(PkSchema, request)

        instance = query_set.get(pk=cls.fix_pk_type(body.pk))
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def delete_many(cls, request: Request) -> Response:
        cls.permit_delete(request)

        query_set = cls._get_query_set(request)
        body = validate_request(PksSchema, request)

        query_set_to_delete = query_set.filter(
            pk__in=[cls.fix_pk_type(pk) for pk in body.pks]
        )
        query_set_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @typing.final
    @classmethod
    def create_router(cls) -> Api:
        root = cls.path_root or cls.model._meta.model_name
        router = Api(f"model/{root}/")

        router.endpoint("pk", method="GET")(cls.get)
        router.endpoint("all", method="GET")(cls.all)
        router.endpoint("where", method="GET")(cls.find)

        router.endpoint("insert", method="POST")(cls.insert)
        router.endpoint("insert-many", method="POST")(cls.insert_many)

        router.endpoint("update", method="PATCH")(cls.update_one)
        router.endpoint("update-many", method="PATCH")(cls.update_many)

        router.endpoint("delete", method="DELETE")(cls.delete_one)
        router.endpoint("delete-manay", method="DELETE")(cls.delete_many)

        return router
