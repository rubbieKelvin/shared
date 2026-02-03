import typing as t

type Pk = int | str
type HTTP_METHODS = t.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
type Json = int | str | bool | float | None | list["Json"] | dict[str, "Json"]
