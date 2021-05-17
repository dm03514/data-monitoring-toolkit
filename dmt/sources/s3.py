import logging

import boto3
from botocore import UNSIGNED
from botocore.config import Config


logger = logging.getLogger(__name__)


def new_from_conf(conf):
    kwargs = {}
    extra_config = conf['storage'].get('config', {})
    signature_version = extra_config.get('signature_version')
    if signature_version == 'UNSIGNED':
        kwargs['config'] = Config(
            signature_version=UNSIGNED
        )
    s3_client = boto3.client('s3', **kwargs)
    return S3(
        client=s3_client
    )


class S3:
    def __init__(self, client):
        self.client = client

    def summary(self, bucket, key):
        paginator = self.client.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=bucket,
            Prefix=key
        )
        total_bytes = 0
        for page in pages:
            for obj in page['Contents']:
                total_bytes += obj['Size']

        logger.info({
            'bucket': bucket,
            'key': key,
            'operation': 'S3.summary',
            'total_bytes': total_bytes
        })
        return total_bytes
