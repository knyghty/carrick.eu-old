from pytest_django.asserts import assertContains


def test_homepage_works(client):
    response = client.get("/")
    assert response.status_code == 200
    assertContains(response, "<title>Tom Carrick</title>")
