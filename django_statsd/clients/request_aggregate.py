from statsd.client import StatsClient

try:
    from django.utils._threading_local import local
except ImportError:
    from threading import local

class AggregateStatsMixin(object):
    aggregate_request_stats = local()

    def timing(self, stat, delta, rate=1):
        super(AggregateStatsMixin, self).timing(stat, delta, rate)
        # view stats only happen once per request so no aggregation necessary
        if stat.startswith('view.'):
            return
        try:
            request = self.aggregate_request_stats.request
            request.stats_timings[stat] += delta
            request.stats_counts[stat] += 1
        except AttributeError:
            pass

class StatsClient(AggregateStatsMixin, StatsClient):
    pass
