"""Accounts admin definitions."""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.

    Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "name"]

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the user with the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.

    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "name", "password", "is_active", "is_staff", "is_superuser"]

    def clean_password(self):
        """Return the initial value regardless of what the user provides."""
        return self.initial["password"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User model admin."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "name", "is_staff", "is_superuser"]
    fieldsets = [
        [None, {"fields": ["email", "name", "password"]}],
        [
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
            },
        ],
        [_("Important dates"), {"fields": ["last_login", "date_joined"]}],
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    )
    search_fields = ["email", "name"]
    ordering = ["name"]
