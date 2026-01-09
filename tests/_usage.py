import typing as t

from django.db import models
from rest_framework.request import Request

from accesscontrol.permissions import FULL_ACCESS
from accesscontrol.roles import RoleSet
from modelview import ModelView


# custom role implementation
class Role(RoleSet[t.Literal["admin", "user"]]):
    @staticmethod
    @t.override
    def getrole(_request: Request):
        return "admin"


# Global roles
adminrole = Role("admin")
userrole = Role("user")


# the model
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()


# model view
class MyModelView(ModelView):
    model = MyModel
    permissions = {
        adminrole: FULL_ACCESS,
        userrole: {
            "select": {
                "mode": "SELECT_ONE_ONLY",
                "rows": models.Q(name="rubbie"),
            }
        },
    }


MyModelView.view()
