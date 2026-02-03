import typing as t

from django.db import models

from accesscontrol.permissions import FULL_ACCESS
from accesscontrol.roles import RoleSet
from modelview import ModelRouter, Request

from ninja import NinjaAPI

api = NinjaAPI()


# the model
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()


type Roles = t.Literal["admin", "user", "anon"]


def get_role(_request: Request) -> Roles:
    print(type(_request))
    return "anon"


# model router
router = (
    ModelRouter[Roles](MyModel)
    .with_queryset(models.Q())
    .with_role_factory(get_role)
    .set_select_permission({"admin": {"rows": models.Q(), "mode": "SELECT_ONE_ONLY"}})
    .build()
)


api.add_router("", router)

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", api.urls),
# ]
