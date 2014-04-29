from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django_statsd.clients import statsd

def model_save(sender, **kwargs):
    instance = kwargs.get('instance')
    statsd.incr('models.%s.%s.%s' % (
        instance._meta.app_label,
        instance._meta.object_name,
        'create' if kwargs.get('created', False) else 'update',
    ))

def model_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    statsd.incr('models.%s.%s.delete' % (
        instance._meta.app_label,
        instance._meta.object_name,
    ))

if getattr(settings, 'STATSD_MODEL_SIGNALS', True):
    post_save.connect(model_save)
    post_delete.connect(model_delete)
