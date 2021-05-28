# data-monitoring-toolkit
Make data observability easy


# Quickstart: Freshness

## Docker-Based

```
$ docker build -t dmt .
$ docker-compose up -d
$ docker run -e DMT_CONN_STRING="postgresql://test:test@host.docker.internal:5432/test" -it dmt --conf=examples/freshness/freshness.yml --type=freshness --db=postgres

2021-05-28 01:22:55,477 - __main__ - INFO - conf: {'freshness': {'targets': [{'database': 'test', 'schema': 'public', 'table': 'test', 'column': 'created_at'}]}}
2021-05-28 01:22:55,478 - datadog.api - INFO - No agent or invalid configuration file found
2021-05-28 01:22:55,571 - dmt.sources.postgres - INFO - Postgres.freshness: executed: SELECT max(created_at) from test.public.test
2021-05-28 01:22:55,576 - dmt.checks.freshness - INFO - freshness table: test.public.test, total_seconds: 105162.590823
```


# Architecture
- checks: executed by the data-monitoring-toolkit script
- sources: concrete data sources which contain metrics, i.e. s3, snowflake, redshift, etc