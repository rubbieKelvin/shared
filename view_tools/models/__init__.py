## Creates view from models
import typing

from pydantic import BaseModel
from django.db.models import Q, QuerySet

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

    def insert(self, data):
        return self.model.objects.create(**data)

    def insert_many(self, data_list):
        instances = [self.model(**data) for data in data_list]
        return self.model.objects.bulk_create(instances)

    def update_one(self, pk, data):
        instance = self.get_one(pk)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def update_many(self, data_list):
        instances = []
        for data in data_list:
            pk = data.pop("pk", None)
            instance = self.get_one(pk)
            for key, value in data.items():
                setattr(instance, key, value)
            instances.append(instance)
        self.model.objects.bulk_update(instances, fields=data.keys())
        return instances

    def delete_one(self, pk):
        instance = self.get_one(pk)
        instance.delete()

    def delete_where(self, **kwargs):
        queryset = self.find_where(**kwargs)
        queryset.delete()

    def delete_many(self, pk_list):
        queryset = self.model.objects.filter(pk__in=pk_list)
        queryset.delete()


class MyModel(AbstractModel):
    pass


class ClassroomView(ModelView[MyModel]):
    model = MyModel
    base_filter_query = None
