import sys
import logging
import traceback


logger = logging.getLogger(__name__)


def handle_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()

    try:
        from raven.contrib.django.raven_compat.models import client
    except ImportError:
        logger.error(''.join(traceback.format_tb(exc_traceback)))
    else:
        client.captureException()
