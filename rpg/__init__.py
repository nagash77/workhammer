import database
import settings
import hashlib
import logging
from importlib import import_module

__version__ = "0.1"
__all__ = ["users", "api", "html"]


def cleanup():
    ''' cleanup:
    Helper function used for testing, cleans up the app's database and
    environment during a testing.
    '''
    database.cleanup()


def password_hash(password):
    pwhash = hashlib.sha224(password)
    pwhash.update(settings.SECRET_KEY)
    return pwhash.hexdigest()


from flask import Flask, request
import rpg.session


class RPGFlask(Flask):
    def __init__(self, *args, **kwargs):
        self.endpoints = {}
        return Flask.__init__(self, *args, **kwargs)

    def endpoint(self, *args, **kwargs):
        def decorator(f):
            self.endpoints[f.__name__] = {
                'url': args[0]
            }
            return self.route(*args, **kwargs)(f)
        return decorator

app = RPGFlask(__name__)
app.session_interface = rpg.session.SessionHandler()
app.jinja_env.line_statement_prefix = '%'
app.debug = settings.DEBUG
app.__version__ = __version__


class logger:
    logger = app.logger
    if app.debug:
        logger.setLevel(logging.DEBUG)

    @classmethod
    def get_extra(cls):
        return {
            'ip': request.environ.get('REMOTE_ADDR', 'x.x.x.x'),
            'url': request.url
        }

    @classmethod
    def debug(cls, *msg):
        if app.config['TESTING']:
            return
        cls.logger.debug(*msg, extra=cls.get_extra())

    @classmethod
    def info(cls, *msg):
        if app.config['TESTING']:
            return
        cls.logger.info(*msg, extra=cls.get_extra())

    @classmethod
    def warning(cls, *msg):
        if app.config['TESTING']:
            return
        cls.logger.warning(*msg, extra=cls.get_extra())

    @classmethod
    def error(cls, *msg):
        if app.config['TESTING']:
            return
        cls.logger.error(*msg, extra=cls.get_extra())

    @classmethod
    def critical(cls, *msg):
        if app.config['TESTING']:
            return
        cls.logger.critical(*msg, extra=cls.get_extra())

for module in __all__:
    import_module("rpg." + module)
