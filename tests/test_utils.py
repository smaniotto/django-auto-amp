import sys

from importlib import reload, import_module

from django.conf import settings
from django.urls import clear_url_caches


def reload_urlconf():
    """
    Reloads Django's urlpatterns definition.
    """
    clear_url_caches()
    urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)


def reload_module(module):
    """
    Reloads a module based on its name.
    """
    imported = import_module(module)
    reload(imported)
