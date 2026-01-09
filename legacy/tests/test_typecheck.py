# test_typecheck.py
from shared.utils.typecheck import isArray, isMap


def test_isArray():
    assert isArray([]) == True
    assert isArray([1, 2, 3]) == True
    assert isArray("") == False
    assert isArray("hello") == False
    assert isArray(123) == False
    assert isArray({"a": 1, "b": 2}) == False


def test_isMap():
    assert isMap({}) == True
    assert isMap({"a": 1, "b": 2}) == True
    assert isMap([]) == False
    assert isMap([1, 2, 3]) == False
    assert isMap("") == False
    assert isMap("hello") == False
    assert isMap(123) == False
