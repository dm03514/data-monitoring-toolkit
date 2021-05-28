import logging

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, metrics, conf, source):
        self.metrics = metrics
        self.conf = conf
        self.source = source

    def execute(self):
        targets = self.conf["storage"]["targets"]
        for target in targets:
            summary = self.source.summary(bucket=target["bucket"], key=target["key"])
            print(summary)

        logger.debug("here")
