import database
import settings
import hashlib
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


import rpg.session
from rpg.decorators import RPGFlask


app = RPGFlask(__name__)
app.session_interface = rpg.session.SessionHandler()
app.jinja_env.line_statement_prefix = '%'
app.debug = settings.DEBUG
app.__version__ = __version__

map(lambda module: import_module("rpg." + module), __all__)
