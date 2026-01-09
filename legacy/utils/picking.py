from .typecheck import isMap
from .typecheck import isArray
from collections.abc import Mapping


def pick(data: Mapping, structure: dict) -> dict:
    """
    Recursively traverses the `structure` dictionary and returns a new dictionary with the same keys as the `structure` dictionary,
    but with the corresponding values from the `data` object. Only keys present in both the `data` and `structure` dictionaries will be included
    in the result.

    Args:
        data (Mapping): A dictionary-like object containing the data to extract keys and values from.
        structure (dict): A dictionary specifying the structure of the desired output. The keys of this dictionary correspond to the keys
        of the returned dictionary, and the values can be either None (to indicate that the corresponding key should be included as-is) or
        another dictionary (to indicate that the corresponding key should be recursively processed).

    Returns:
        dict: A new dictionary with the same keys as the `structure` dictionary, but with the corresponding values from the `data` object.

    Raises:
        KeyError: If any key in the `structure` dictionary is not present in the `data` object.
    """

    res = {}
    for key, val in structure.items():
        if not (key in data):
            raise KeyError(f"{key} doenst exist in root")

        if val:
            if isMap(data[key]):
                if isMap(val):
                    res[key] = pick(data[key], val)
                else:
                    res[key] = data[key]
            elif isArray(data[key]):
                res[key] = [pick(i, val) if isMap(val) else i for i in data[key]]
            else:
                res[key] = data[key]

    return res
