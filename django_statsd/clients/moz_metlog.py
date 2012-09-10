from statsd.client import StatsClient


class StatsClient(StatsClient):
    """A client that pushes messages to metlog """

    def __init__(self, *args, **kw):
        super(StatsClient, self).__init__(*args, **kw)
        try:
            from django.conf import settings
            self.metlog = settings.METLOG
        except (ImportError, AttributeError):
            METLOG_CONF = {
                'logger': 'django-statsd',
                'sender': {
                    'class': 'metlog.senders.logging.StdLibLoggingSender',
                    'logger_name': None
                },
            }
            from metlog.config import client_from_dict_config
            self.metlog = client_from_dict_config(METLOG_CONF)

    def timing(self, stat, delta, rate=1):
        """Send new timing information. `delta` is in milliseconds."""
        self.metlog.timer_send(stat, delta, rate=rate)

    def incr(self, stat, count=1, rate=1):
        """Increment a stat by `count`."""
        self.metlog.incr(stat, count, rate=rate)

    def decr(self, stat, count=1, rate=1):
        """Decrement a stat by `count`."""
        self.metlog.incr(stat, -count, rate=rate)
