from django.conf import settings


def get_logo():
    with open(
        settings.BASE_DIR / "carrick" / "static" / "carrick" / "img" / "logo.svg"
    ) as f:
        return f.read()


def show_toolbar(request):
    return (
        settings.ENABLE_DEBUG_TOOLBAR
        and request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
    )
