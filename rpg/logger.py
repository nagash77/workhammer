import logging
from flask import request
from rpg import app


logger = app.logger
if app.debug:
    logger.setLevel(logging.DEBUG)


def __get_extra():
    return {
        'ip': request.environ.get('REMOTE_ADDR', 'x.x.x.x'),
        'url': request.url
    }


def debug(*msg):
    if app.config['TESTING']:
        return
    logger.debug(*msg, extra=__get_extra())


def info(*msg):
    if app.config['TESTING']:
        return
    logger.info(*msg, extra=__get_extra())


def warning(*msg):
    if app.config['TESTING']:
        return
    logger.warning(*msg, extra=__get_extra())


def error(*msg):
    if app.config['TESTING']:
        return
    logger.error(*msg, extra=__get_extra())


def critical(*msg):
    if app.config['TESTING']:
        return
    logger.critical(*msg, extra=__get_extra())
