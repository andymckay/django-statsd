from django.core import cache
from django.core.cache.backends.base import BaseCache

from django_statsd.patches.utils import wrap


def key(cache, attr):
    return 'cache.%s.%s' % (cache.__module__.split('.')[-1], attr)


class StatsdTracker(BaseCache):

    def __init__(self, cache):
        self.cache = cache

    def __getattribute__(self, attr):
        if attr == 'cache':
            return BaseCache.__getattribute__(self, attr)
        # Don't wrap default_timeout in a functools.partial object (see wrap)
        # This ensures compatibility with django-parler 1.6 under Django 1.9
        if attr == 'default_timeout':
            return self.cache.default_timeout
        return wrap(getattr(self.cache, attr), key(self.cache, attr))


def patch():
    cache.cache = StatsdTracker(cache.cache)
