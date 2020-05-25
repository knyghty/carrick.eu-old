from django.contrib import sitemaps
from django.urls import reverse


static_pages = {"home": {"changefreq": "weekly", "priority": 1.0}}


class StaticViewSitemap(sitemaps.Sitemap):
    protocol = "https"

    def changefreq(self, item):
        return static_pages.get(item, {}).get("changefreq", "monthly")

    def items(self):
        return list(static_pages.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return static_pages.get(item, {}).get("priority", 0.5)
