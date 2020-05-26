import pytest
from pytest_django.asserts import assertContains


def test_homepage_works(client):
    response = client.get("/")
    assert response.status_code == 200
    assertContains(response, "<title>Tom Carrick</title>")


@pytest.mark.django_db
def test_sitemap_has_homepage(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assertContains(response, "<loc>https://carrick.eu/</loc>")
