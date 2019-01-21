import threading

from statsd.client import StatsClient

from django.conf import settings
from django.utils.functional import lazy

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

thread_local = threading.local()


def get(name, default):
    try:
        return getattr(settings, name, default)
    except ImportError:
        return default


def get_client():
    client = get('STATSD_CLIENT', 'statsd.client')
    host = get('STATSD_HOST', 'localhost')
# This is causing problems with statsd
# gaierror ([Errno -9] Address family for hostname not supported)
# TODO: figure out what to do here.
#    host = socket.gethostbyaddr(host)[2][0]
    port = get('STATSD_PORT', 8125)
    prefix = get('STATSD_PREFIX', None)
    return import_module(client).StatsClient(host=host, port=port, prefix=prefix)


def _get_client():
    if not hasattr(thread_local, 'django_statsd_client'):
        thread_local.django_statsd_client = get_client()
    return thread_local.django_statsd_client


statsd = lazy(_get_client, StatsClient)()
