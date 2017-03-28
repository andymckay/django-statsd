

from django_statsd.clients import statsd
import time

_task_start_times = {}


def on_before_task_publish(sender=None, **kwds):
    """
    Handle Celery ``before_task_publish`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.before_task_publish' % sender.replace('.', '_'))


def on_after_task_publish(sender=None, **kwds):
    """
    Handle Celery ``after_task_publish`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.after_task_publish' % sender.replace('.', '_'))


def on_task_prerun(sender=None, task_id=None, **kwds):
    """
    Handle Celery ``task_prerun``signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.start' % sender.name.replace('.', '_'))

    # Keep track of start times. (For logging the duration in the postrun.)
    _task_start_times[task_id] = time.time()


def on_task_postrun(sender=None, task_id=None, **kwds):
    """
    Handle Celery ``task_postrun`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.done' % sender.name.replace('.', '_'))

    # Log duration.
    start_time = _task_start_times.pop(task_id, False)
    if start_time:
        ms = int((time.time() - start_time) * 1000)
        statsd.timing('celery.%s.runtime' % sender.name.replace('.', '_'), ms)


def on_task_success(sender=None, **kwds):
    """
    Handle Celery ``task_success`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.success' % sender.name.replace('.', '_'))


def on_task_failure(sender=None, task_id=None, task=None, **kwds):
    """
    Handle Celery ``task_failure`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.failure' % sender.name.replace('.', '_'))


def on_task_retry(sender=None, **kwds):
    """
    Handle Celery ``task_retry`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.retry' % sender.name.replace('.', '_'))


def on_task_revoked(sender=None, **kwds):
    """
    Handle Celery ``task_revoked`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.revoked' % sender.name.replace('.', '_'))


def on_task_unknown(sender=None, name=None, **kwds):
    """
    Handle Celery ``task_unknown`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.unknown' % name.replace('.', '_'))


def on_task_rejected(sender=None, **kwds):
    """
    Handle Celery ``task_rejected`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.rejected')


def register_celery_events():
    try:
        from celery import signals
    except ImportError:
        raise ImportError('Cannot import celery.signals. This dependency is required when STATSD_CELERY_SIGNALS'
                          ' is True.')
    else:
        signals.before_task_publish.connect(on_before_task_publish)
        signals.after_task_publish.connect(on_after_task_publish)
        signals.task_prerun.connect(on_task_prerun)
        signals.task_postrun.connect(on_task_postrun)
        signals.task_success.connect(on_task_success)
        signals.task_failure.connect(on_task_failure)
        signals.task_retry.connect(on_task_retry)
        signals.task_revoked.connect(on_task_revoked)
        signals.task_unknown.connect(on_task_unknown)
        signals.task_rejected.connect(on_task_rejected)
