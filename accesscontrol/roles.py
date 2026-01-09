from rest_framework.request import Request


class RoleSet[T: str]:
    """Classes that limits access to certain resources"""

    _roleset: set[T] = set()

    def __init__(self, name: T):
        self.name = name
        if name in self._roleset:
            raise ValueError(f"Duplicate role: {name}")
        self._roleset.add(name)

    @staticmethod
    def getrole(_request: Request) -> T:
        """Verifies that a user is a certain role"""
        raise NotImplementedError
