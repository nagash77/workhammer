import database
import settings
import hashlib
from importlib import import_module

__version__ = "0.1"
__all__ = ["users", "api"]


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


from flask import Flask
import rpg.session


class RPGFlask(Flask):
    def __init__(self, *args, **kwargs):
        self.endpoints = {}
        return Flask.__init__(self, *args, **kwargs)

    def endpoint(self, *args, **kwargs):
        def decorator(f):
            self.endpoints[f.__name__] = {
                'url': args[0],
                'methods': kwargs.get('methods', ['GET'])
            }
            return self.route(*args, **kwargs)(f)
        return decorator

app = RPGFlask(__name__)
app.session_interface = rpg.session.SessionHandler()
app.debug = settings.DEBUG
app.__version__ = __version__

for module in __all__:
    import_module("rpg." + module)
