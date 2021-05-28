import logging

import click
from datadog import initialize, statsd
import yaml

from dmt import checks
from dmt.sources import s3, postgres


logger = logging.getLogger(__name__)


def init_logging():
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def init_check(cli_args):
    conf = yaml.load(cli_args['conf'], Loader=yaml.FullLoader)
    logger.info('conf: {}'.format(conf))

    options = {
        "statsd_host": "127.0.0.1",
        "statsd_port": 8125,
    }
    initialize(**options)

    if cli_args['type'] == 'storage':
        if cli_args['db'] == 's3':
            source = s3.new_from_conf(conf)

        print(conf)
        check = checks.Storage(
            metrics=statsd,
            conf=conf,
            source=source
        )

    elif cli_args['type'] == 'freshness':

        if cli_args['db'] == 'postgres':
            source = postgres.new_from_conf(
                conn_string=cli_args['conn_string'],
                conf=conf,
            )

        check = checks.Freshness(
            metrics=statsd,
            conf=conf,
            source=source,
        )

    return check


@click.command()
@click.option(
    '--conn-string',
    help='connection string for the db'
)
@click.option(
    '--db',
    type=click.Choice(['s3', 'postgres']),
    default='postgres',
    help='which db backend'
)
@click.option(
    '--conf',
    type=click.File('rb'),
    help='configuration file to use for monitoring'
)
@click.option(
    '--type',
    type=click.Choice(['storage', 'freshness']),
    help='check type, need to figure out clean subcommands'
)
def main(**kwargs):
    init_logging()
    check = init_check(kwargs)
    return check.execute()


if __name__ == '__main__':
    main(auto_envvar_prefix='DMT')
