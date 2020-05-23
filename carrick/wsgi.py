"""WSGI config for carrick.eu."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carrick.settings")

application = get_wsgi_application()
