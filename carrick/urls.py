"""carrick.eu URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from . import sitemaps


sitemaps = {
    "static": sitemaps.StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", flatpage, {"url": "/"}, name="home"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:  # pragma: nocover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
