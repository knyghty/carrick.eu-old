from django.contrib.sites.models import Site

import pytest
from model_bakery import baker
from pytest_django.asserts import assertContains


@pytest.mark.django_db
def test_homepage_has_title_and_strapline(client):
    baker.make(
        "flatpages.FlatPage",
        url="/",
        title="Tom Carrick",
        content="test content",
        sites=Site.objects.filter(domain="carrick.eu"),
        template_name="flatpages/home.jinja2",
    )
    response = client.get("/", secure=True)
    assert response.status_code == 200
    assertContains(response, "<title>Tom Carrick</title>")
    assertContains(response, '<span class="strapline">')


@pytest.mark.django_db
def test_sitemap_has_homepage(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assertContains(response, "<loc>https://carrick.eu/</loc>")
