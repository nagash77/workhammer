import logging
from flask import request
from rpg import app

FORMAT = '%(asctime)-11s %(ip)-15s %(url)s: %(message)s'

logger = app.logger
logging.basicConfig(format=FORMAT)
if app.debug:
    logger.setLevel(logging.DEBUG)
    app.debug_log_format = FORMAT


def __get_extra():
    return {
        'ip': request.environ.get('REMOTE_ADDR', 'x.x.x.x'),
        'url': request.url
    }


def debug(*msg):
    logger.debug(*msg, extra=__get_extra())


def info(*msg):
    logger.info(*msg, extra=__get_extra())


def warning(*msg):
    logger.warning(*msg, extra=__get_extra())


def error(*msg):
    logger.error(*msg, extra=__get_extra())


def critical(*msg):
    logger.critical(*msg, extra=__get_extra())
