from .toolbar import StatsClient as ToolbarStatsClient
from .request_aggregate import AggregateStatsMixin

class StatsClient(AggregateStatsMixin, ToolbarStatsClient):
    pass
