import logging
from pagerglue.methods.base import PageMethod

logger = logging.getLogger(__name__)


class Log(PageMethod):
    def send_message(self, message):
        logger.warning(message)
