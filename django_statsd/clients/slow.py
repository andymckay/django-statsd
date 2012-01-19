import statsd


def send_bulk_stats(*a, **kw):
    from django_statsd.clients import statsd
    statsd.send_bulk()


class StatsClient(statsd.StatsClient):
    request_finished = send_bulk_stats
    _bulk_stats = []

    def _send(self, stat, value, rate):
        """Instead of sending immediately, capture stats to send later."""
        self._bulk_stats.append((stat, value, rate))

    def reset_bulk(self):
        """Reset the captured stats."""
        self._bulk_stats = []

    def send_bulk(self):
        """Send all captured stats."""
        for stat, value, rate in self._bulk_stats:
            super(StatsClient, self)._send(stat, value, rate)
        self.reset_bulk()
