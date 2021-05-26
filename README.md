# data-monitoring-toolkit
Make data observability easy


# Quickstart: Freshness
```
$ docker-compose up -d
$ DMT_CONN_STRING="postgresql://test:test@localhost:5432/test" python cmd/data-monitoring-toolkit.py --conf=examples/freshness/freshness.yml --type=freshness --db=postgres
```


# Architecture
- checks: executed by the data-monitoring-toolkit script
- sources: concrete data sources which contain metrics, i.e. s3, snowflake, redshift, etc