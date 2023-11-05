import string
from nanoid import non_secure_generate

from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from shared.abstractmodel import AbstractModel, serialization, utils


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str, **extra_fields: str | bool | None
    ) -> "ExtensibleUser":
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The email must be set")

        email = self.normalize_email(email)

        # more validation
        # ...

        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(
        self, email: str, password: str, **extra_fields: str | bool | None
    ) -> "ExtensibleUser":
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        return self.create_user(email, password, **extra_fields)


class ExtensibleUser(AbstractModel, AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, help_text="User's email address")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: UserManager = UserManager()

    class Meta:
        abstract = True

    @property
    def fullname(self) -> str:
        return self.get_full_name()

    @property
    def serializers(
        self,
    ) -> tuple[
        serialization.SerializationStructure,
        dict[str, serialization.SerializationStructure],
    ]:
        all_fields = utils.getAllModelFields(self.__class__)
        exempt_fields = ["password"]

        return serialization.struct(*set(all_fields).difference(exempt_fields)), {
            "simple": serialization.struct("id", "first_name", "last_name", "email"),
            "identifier_only": serialization.struct("id", "email"),
        }

    def __str__(self) -> str:
        return self.email


useable_chars = string.ascii_letters + string.digits


def default_code_gen() -> str:
    return non_secure_generate(useable_chars, size=12)


class CallbackInformation(AbstractModel):
    code = models.CharField(max_length=12, default=default_code_gen)
    token = models.TextField()
