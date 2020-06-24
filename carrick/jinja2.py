from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment
from snakeoil.jinja2 import get_meta_tags

from .utils import get_logo


def environment(**options):
    env = Environment(lstrip_blocks=True, trim_blocks=True, **options)
    env.globals.update(
        {
            "get_meta_tags": get_meta_tags,
            "logo": get_logo(),
            "static": static,
            "url": reverse,
        }
    )
    return env
