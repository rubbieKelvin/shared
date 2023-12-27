## Creates view from models
import typing

from pydantic import BaseModel
from django.db.models import Q, QuerySet

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from shared.utils.query import makeQuery
from shared.abstractmodel import AbstractModel

from ..body_tools import validate_request
from ..exceptions import ResourceNotFound
from ..pagination import paginate_by_queryparam, paginate

from .schemas import *
from .typedefs import *
from .mixins import PermissionMixin


class ModelView[T: AbstractModel](PermissionMixin):
    model: type[T]
    base_filter_query: Q | None = None
    must_update_fields: list[str] = [
        "last_updated"
    ]  # fields that must be updated when updating model

    insert_schema: type[BaseModel]
    update_schema: type[UpdateOneSchema]
    update_many_schema: type[UpdateManySchema]
    insert_many_schema: type[InsertManySchema]

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
        body = validate_request(GetOneSchema, request)

        # get row scope
        query_set = cls._get_query_set(request)

        # get instance
        try:
            instance = query_set.get(pk=body.pk)
        except cls.model.DoesNotExist:
            raise ResourceNotFound(
                f"f{cls.model.__class__.__name__}({body.pk}) not found"
            )

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

        queryset = cls._get_query_set(request)
        instance = queryset.get(pk=body.pk)
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
            instance = query_set.get(pk=pk)

            for key, value in set_.items():
                setattr(instance, key, value)

            instances.append(instance)

        cls.model.objects.bulk_update(
            instances, fields=[*set_.keys(), *cls.must_update_fields]
        )

        return Response([cls.serializer_func(i, "UPDATE_MANY") for i in instances])

    def delete_one(self, pk):
        instance = self.get_one(pk)
        instance.delete()

    def delete_many(self, pk_list):
        queryset = self.model.objects.filter(pk__in=pk_list)
        queryset.delete()


class MyModel(AbstractModel):
    pass


class ClassroomView(ModelView[MyModel]):
    model = MyModel
    base_filter_query = None
