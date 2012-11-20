import database
import settings
import hashlib
from importlib import import_module

__version__ = "0.1"
# List of the modules to import
__all__ = ["users", "players", "api", "html"]


def cleanup():
    ''' cleanup:
    Helper function used for testing, cleans up the app's database and
    environment during a testing.
    '''
    database.cleanup()


def password_hash(password):
    ''' password_hash:
    Application wide hashing function for passwords, just salts and hashes the
    password and returns a hex representation of the hash.
    '''
    pwhash = hashlib.sha224(password)
    pwhash.update(settings.SECRET_KEY)
    return pwhash.hexdigest()


def filter_keys(src, blacklist):
    ''' filter_keys
    Helper function, removes the (key, value) pairs for keys in the blacklist
    list, returns filtered dictionary.
    '''
    for key in blacklist:
        if key in src:
            del src[key]

    return src

# Webapp initialization
import session
from .decorators import RPGFlask

# RPGFlask is in decorators and is just an extended version of flask.Flask
app = RPGFlask(__name__)
app.session_interface = session.SessionHandler()
app.jinja_env.line_statement_prefix = '%'
app.debug = settings.DEBUG
app.__version__ = __version__
# This just imports all of the webapps modules (defined in __all__)
map(lambda module: import_module("." + module, __name__), __all__)
