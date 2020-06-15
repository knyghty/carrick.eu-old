from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from .utils import get_logo


def environment(**options):
    env = Environment(**options)
    env.globals.update({"logo": get_logo(), "static": static, "url": reverse})
    return env
