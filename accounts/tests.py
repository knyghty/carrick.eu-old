from django.contrib.postgres.fields import CIEmailField

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import from_model, register_field_strategy
from model_bakery import baker

from .admin import UserChangeForm, UserCreationForm
from .models import User


register_field_strategy(CIEmailField, st.emails())


@pytest.mark.django_db
@given(from_model(User))
def test_user_string_matches_name(user):
    assert str(user) == user.name


@pytest.mark.django_db
def test_user_can_be_created_from_admin_form():
    form = UserCreationForm(
        {
            "name": "César Peña",
            "email": "cesar@example.com",
            "password1": "correcthorsebatterystaple",
            "password2": "correcthorsebatterystaple",
        }
    )
    assert form.is_valid() is True
    form.save()
    assert User.objects.filter(email="cesar@example.com").exists()


@pytest.mark.django_db
def test_user_cannot_be_created_with_mismatched_password():
    form = UserCreationForm(
        {
            "name": "末弘 秀孝",
            "email": "swery65@example.com",
            "password1": "correcthorsebatterystaple",
            "password2": "incorrecthorsebatterystaple",
        }
    )
    assert form.is_valid() is False
    assert form.errors["password2"][0] == "Passwords don't match"


@pytest.mark.django_db
def test_cannot_create_users_with_non_unique_passowrds():
    """
    Test that user emails must be unique.

    Since the User model uses `CIEmailField`, it tests with the same email
    but with different cases.
    """
    baker.make(User, email="random@example.com")
    form = UserCreationForm(
        {
            "name": "Random Hajile",
            "email": "Random@example.com",
            "password1": "correcthorsebatterystaple",
            "password2": "correcthorsebatterystaple",
        }
    )
    assert form.is_valid() is False
    assert form.errors["email"][0] == "User with this Email address already exists."


@pytest.mark.django_db
def test_can_create_user_without_saving():
    form = UserCreationForm(
        {
            "name": "Sari Sari",
            "email": "sari@example.com",
            "password1": "correcthorsebatterystaple",
            "password2": "correcthorsebatterystaple",
        }
    )
    assert form.is_valid() is True
    form.save(commit=False)
    assert User.objects.filter(email="sari@example.com").exists() is False


@pytest.mark.django_db
def test_cannot_change_user_password_from_admin_change_form():
    user = baker.make(User)
    form = UserChangeForm(
        data={"email": user.email, "name": user.name, "password": "trustno1"},
        instance=user,
    )
    assert form.is_valid() is True
    saved_user = form.save()
    assert saved_user.password == user.password


@pytest.mark.django_db
def test_cannot_create_user_without_name():
    with pytest.raises(ValueError):
        User.objects.create_user(email="anonymous@example.com", name="")


@pytest.mark.django_db
def test_cannot_create_user_without_email():
    with pytest.raises(ValueError):
        User.objects.create_user(email="", name="Anonymous")


@pytest.mark.django_db
def test_created_user_is_not_staff():
    user = User.objects.create_user(email="salem@example.com", name="سالم حنا خميس")
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(email="grace@example.com", name="Grace Hopper")
    assert user.is_staff is True
    assert user.is_superuser is True
