"""carrick.eu URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [path("admin/", admin.site.urls), path("", views.HomeView.as_view())]

if settings.DEBUG:  # pragma: nocover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
