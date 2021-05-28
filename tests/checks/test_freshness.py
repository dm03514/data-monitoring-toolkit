import unittest
from unittest import mock
from datetime import datetime

from dmt.checks.freshness import Freshness


class FreshnessTestCase(unittest.TestCase):
    def test_emit_gauge(self):
        metrics = mock.MagicMock()
        freshness = Freshness(metrics=metrics, conf=None, source=None)
        freshness._emit(
            {
                "database": "testdb",
                "schema": "testschema",
                "table": "testtable",
            },
            last_update=datetime(year=2020, month=8, day=1),
            now_fn=lambda: datetime(year=2020, month=8, day=2),
        )
        metrics.gauge.assert_called_once_with(
            "dmt.freshness.table.total_seconds",
            86400.0,
            ["db:testdb", "schema:testschema", "table:testtable"],
            1,
        )

    def test_tags_with_extra_tags(self):
        freshness = Freshness(metrics=None, conf=None, source=None)
        self.assertEqual(
            [
                "db:testdb",
                "schema:testschema",
                "table:testtable",
                "service:testservice",
                "target:testtarget",
            ],
            freshness._tags(
                target={
                    "database": "testdb",
                    "schema": "testschema",
                    "table": "testtable",
                    "tags": ["service:testservice", "target:testtarget"],
                }
            ),
        )
