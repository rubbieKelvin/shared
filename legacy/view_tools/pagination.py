import typing
from pydantic import BaseModel
from rest_framework.request import Request
from django.db.models import QuerySet, Manager

I = typing.TypeVar("I", list, tuple, QuerySet, Manager, covariant=True)


class PaginationData(BaseModel):
    offset: int = 0
    limit: int = 100


def paginate(iterable: I, limit: int, offset: int) -> I:
    offset = offset * limit
    paginated_list = iterable[offset : offset + limit]
    return paginated_list


def paginate_by_queryparam(request: Request, iterable: I) -> I:
    params = request.query_params
    offset = params.get("pagination_offset", "0")
    limit = params.get("pagination_limit", "10")

    pagination_data = PaginationData(offset=offset, limit=limit)  # type: ignore
    return paginate(
        iterable, limit=pagination_data.limit, offset=pagination_data.offset
    )
