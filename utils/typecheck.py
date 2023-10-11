from collections.abc import Sequence
from collections.abc import Mapping
from django.db import models


def isArray(x) -> bool:
    return (isinstance(x, Sequence) and type(x) != str) or isinstance(
        x, models.QuerySet
    )


def isMap(x) -> bool:
    return isinstance(x, Mapping)
