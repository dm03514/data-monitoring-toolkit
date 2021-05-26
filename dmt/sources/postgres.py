import logging
from sqlalchemy import create_engine

from dmt.checks.freshness import TableFreshness


logger = logging.getLogger(__name__)


def new_from_conf(conn_string, conf):
    db = create_engine(conn_string)
    conn = db.connect()
    return Postgres(
        client=conn,
    )


class Postgres:
    def __init__(self, client):
        self.client = client

    def freshness(self, target) -> TableFreshness:
        sql = 'SELECT max({}) from {}.{}.{}'.format(
            target['column'],
            target['database'],
            target['schema'],
            target['table']
        )
        logger.info('Postgres.freshness: executed: {}'.format(sql))
        result = self.client.execute(sql)
        return result.first()[0]
