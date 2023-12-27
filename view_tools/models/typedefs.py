import typing

MODEL_VIEW_ACTIONS = typing.Literal[
    "ALL",
    "GET",
    "FIND",
    "CREATE",
    "UPDATE_ONE",
    "UPDATE_WHERE",
    "DELETE",
    "DELETE_WHERE",
    "DELETE_MANY",
]
