from typing import cast
from django.db import models


def RELATED_QUERYSET_RESOLVER(object: models.Model, property: str) -> models.QuerySet:
    """
    Resolve a related queryset from a Django model object based on the provided property name.

    Args:
        object (models.Model): The Django model instance from which to retrieve the related queryset.
        property (str): The name of the property that represents the related field or manager.

    Returns:
        models.QuerySet: The queryset containing related objects.

    Example:
        Given a model instance `user` with a related field called `posts`:
        posts_queryset = RELATED_QUERYSET_RESOLVER(user, 'posts')
        This will retrieve all related posts for the user.
    """

    related_set = cast(models.manager.RelatedManager, getattr(object, property))
    assert isinstance(
        related_set, models.manager.RelatedManager
    ), f"{property} is not a RelatedManager"
    return related_set.all()
