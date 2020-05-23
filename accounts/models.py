"""Accounts models."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(DjangoUserManager):
    def create_user(
        self, email, name, password=None, is_staff=False, is_superuser=False
    ):
        """Create a :model:`accounts.User`."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not name:
            raise ValueError("Users must have a name.")

        user = self.model(
            email=email, name=name, is_staff=is_staff, is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """Create and save a superuser."""
        return self.create_user(
            email=email, name=name, password=password, is_staff=True, is_superuser=True
        )


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model. Uses email for logging in and a single `name` field."""

    email = CIEmailField(verbose_name="email address", primary_key=True)
    name = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
