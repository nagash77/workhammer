import database
import settings
import hashlib
from importlib import import_module

__version__ = "0.1"
__all__ = ["users", "players", "api", "html"]  # List of the modules to import


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

# Webapp initialization
import rpg.session
from rpg.decorators import RPGFlask

# RPGFlask is in decorators and is just an extended version of flask.Flask
app = RPGFlask(__name__)
app.session_interface = rpg.session.SessionHandler()
app.jinja_env.line_statement_prefix = '%'
app.debug = settings.DEBUG
app.__version__ = __version__
# This just imports all of the webapps modules (defined in __all__)
map(lambda module: import_module("rpg." + module), __all__)
