import typing as t
from collections.abc import Sequence

from django.db.models import Manager, QuerySet


class Pagination(t.TypedDict):
    offset: int
    limit: int


def paginate[T: Sequence[t.Any] | QuerySet[t.Any]](
    iterable: T, config: Pagination
) -> T:
    limit = config.get("limit", 100)
    offset = config.get("offset", 0)

    start = offset * limit
    stop = start + limit

    # Logic fix: Managers must be converted to QuerySets to be sliced
    if isinstance(iterable, Manager):
        return t.cast(T, iterable.all()[start:stop])

    return t.cast(T, iterable[start:stop])
