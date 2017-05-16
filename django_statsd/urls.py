from django_statsd.views import record

try:
    from django.conf.urls import url
    urlpatterns = [
    r'',
    url(r'^record$', record, name='django_statsd.record'),
    ]

except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url
    urlpatterns = patterns(
        '',
        url(r'^record$', 'django_statsd.views.record', name='django_statsd.record'),
    )
