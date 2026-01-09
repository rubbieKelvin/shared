import json
import typing
from functools import wraps


def cached(
    input_serializer: typing.Callable[
        [typing.Sequence[typing.Any], dict[str, typing.Any]], str
    ] = lambda args, kwargs: json.dumps({"args": args, "kwargs": kwargs})
):
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = input_serializer(args, kwargs)
            if key in cache:
                return cache[key]

            res = func(*args, **kwargs)
            cache[key] = res
            return res

        return wrapper

    return decorator
