FROM python:3.9-slim-buster

WORKDIR /usr/src/dmt

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates

RUN update-ca-certificates

COPY . .

RUN pip install -r requirements.txt
RUN python setup.py install

RUN useradd -m dmt
USER dmt

ENTRYPOINT [ "python", "./cmd/data-monitoring-toolkit.py" ]