from django.db import models
from uuid import uuid4


class AbstractModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
