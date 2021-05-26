from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TableFreshness:
    pass


class Freshness:
    def __init__(self, metrics, conf, source):
        self.metrics = metrics
        self.conf = conf
        self.source = source

    def execute(self):
        targets = self.conf['freshness']['targets']
        for target in targets:
            last_update = self.source.freshness(target)
            self._emit(target, last_update)

    def _emit(self, target, last_update):
        now = datetime.utcnow()
        diff = now - last_update
        logger.info('freshness table: {}.{}.{}, total_seconds: {}'.format(
            target['database'],
            target['schema'],
            target['table'],
            diff.total_seconds(),
        ))

        tags = [
            'db:{}'.format(target['database']),
            'schema:{}'.format(target['schema']),
            'table:{}'.format(target['table']),
        ]
        tags.extend(target.get('tags', []))

        self.metrics.gauge(
            'dmt.freshness.table.total_seconds',
            diff.total_seconds(),
            tags,
            1,
        )
