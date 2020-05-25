import functools

import pytest


@pytest.fixture
def client(client):
    """
    Return a client that always works with SSL.

    This removes the need to turn `SECURE_SSL_REDIRECT` off during tests.
    """
    client.get = functools.partial(client.get, secure=True)
    client.post = functools.partial(client.post, secure=True)
    return client
