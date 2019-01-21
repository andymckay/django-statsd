from django.apps import AppConfig
from django.conf import settings


class StatsdAppConfig(AppConfig):
    name = 'django_statsd'

    def ready(self):
        if getattr(settings, 'STATSD_CELERY_SIGNALS', False):
            from django_statsd.handlers.celery import register_celery_events

            register_celery_events()

        if getattr(settings, 'STATSD_MODEL_SIGNALS', False):
            from django_statsd.handlers.models import register_model_signals

            register_model_signals()
