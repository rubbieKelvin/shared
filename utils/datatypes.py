import typing

I = typing.TypeVar("I")
T = typing.TypeVar("T")


def safeNumber(
    value: str | float | int | None, default: float | int = 0
) -> int | float:
    """
    Convert a value to a valid number or return a default value.

    This function takes a value, which can be a string, float, or integer, and attempts to convert it to a valid number.
    If the conversion is successful, the function returns the number as an integer if it has no decimal places (i.e., it's an integer).
    Otherwise, it returns the number as a float.

    If there's any error during the conversion or if the input value is not a valid number, the function returns the default value.

    Parameters:
        value (str | float | int): The value to be converted to a number. It can be a string representation of a number,
            a float, or an integer.
        default (float | int, optional): The default value to be returned if there's an error during conversion.
            Default is 0.

    Returns:
        int | float: The converted number if the conversion is successful and it's a valid number, otherwise the default value.

    Example:
        print(safeNumber("4.2"))  # Output: 4 (converted to integer)

        # Conversion successful - the input is a valid float
        print(safeNumber(3.14))  # Output: 3.14 (remains as float)

        # Conversion successful - the input is a valid integer
        print(safeNumber(100))  # Output: 100 (converted to integer)

        # Conversion failed - the input is not a valid number
        print(safeNumber("abc"))  # Output: 0 (default value returned)

        # Conversion failed - the input is None
        print(safeNumber(None))  # Output: 0 (default value returned)

        # Conversion failed - the input is a list
        print(safeNumber([1, 2, 3]))  # Output: 0 (default value returned)"""

    if value == None:
        return default

    try:
        # Attempt to convert the input to a float
        number = float(value)
        # Check if the number has no decimal places (i.e., it's an integer)
        if number.is_integer():
            return int(number)  # Return the number as an integer
        else:
            return number  # Return the number as a float
    except (ValueError, TypeError):
        # Return 0 if there's an error during conversion
        return default


def paginate(
    iter: I,
    limit: int | None = None,
    page: int = 0,
) -> I:
    """Paginate a sequence.

    This function takes a sequence of elements of type `I` and returns a paginated version of it
    based on the specified limit and page number. If the limit is not provided, the entire sequence will be returned.

    Parameters:
        iter (I): The input sequence to be paginated.
            The generic type `I` represents either a standard sequence (e.g., list, tuple).
            It allows for flexible input, and the return type will preserve the input type.
        limit (int | None, optional): The maximum number of elements per page. Default is None.
            If not specified, the entire input sequence will be returned.
        page (int, optional): The page number of the paginated sequence to return. Default is 0,
            which represents the first page.

    Returns:
        I: A paginated sequence containing the elements of the input.

    Example:
        data = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Paginate data with a limit of 3 elements per page
        page_1 = paginate(data, limit=3, page=0)  # [0, 1, 2]
        page_2 = paginate(data, limit=3, page=1)  # [3, 4, 5]
        page_3 = paginate(data, limit=3, page=2)  # [6, 7, 8]
        page_4 = paginate(data, limit=3, page=3)  # [9]

        # No pagination when limit is not provided
        all_data = paginate(data)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    if limit:
        offset = page * limit
        return iter[offset : offset + limit]  # type: ignore
    return iter


def find(arr: typing.Sequence[T], finder: typing.Callable[[T], bool]) -> T | None:
    """
    Find the first element in the given sequence that satisfies the condition specified by the finder function.

    The function iterates through each element in the sequence and applies the finder function to it.
    If the finder function returns True for an element, that element is considered as the match, and the function
    returns it immediately. If no element satisfies the condition, the function returns None.

    Args:
        arr (typing.Sequence[T]): The sequence of elements to search for a match.
        finder (typing.Callable[[T], bool]): A callable function that takes an element from the sequence as input and
                                              returns True if the element satisfies the desired condition, otherwise False.

    Returns:
        T or None: The first element that satisfies the condition specified by the finder function,
                   or None if no such element is found.

    Examples:
        >>> def is_even(n: int) -> bool:
        ...     return n % 2 == 0

        >>> numbers = [1, 3, 5, 8, 10, 12]
        >>> find(numbers, is_even)
        8

        >>> find(numbers, lambda x: x > 15)
        None
    """
    for i in arr:
        if finder(i):
            return i
    return None


def booleanString(value: str) -> bool:
    """
    Convert a string to a boolean value.

    This function takes a string and attempts to convert it to a boolean value.
    If the conversion is successful, the function returns True if the string is "true" (case-insensitive).
    Otherwise, it returns False.

    Parameters:
        value (str): The string to be converted to a boolean value.

    Returns:
        bool: True if the string is "true" (case-insensitive), otherwise False.

    Example:
        print(booleanString("true"))  # Output: True
        print(booleanString("True"))  # Output: True
        print(booleanString("TRUE"))  # Output: True
        print(booleanString("false"))  # Output: False
        print(booleanString("abc"))  # Output: False
        print(booleanString("123"))  # Output: False
        print(booleanString(""))  # Output: False
        print(booleanString(None))  # Output: False
    """
    true_aliases = ["true", "yes", "1", "y"]
    return value.lower() in true_aliases
