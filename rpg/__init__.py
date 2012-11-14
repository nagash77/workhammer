import database
import settings
import hashlib
from importlib import import_module

__version__ = "0.1"
__all__ = ["users"]


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

app = Flask(__name__)
app.session_interface = rpg.session.SessionHandler()

for module in __all__:
    import_module("rpg." + module)

if __name__ == '__main__':
    app.run()
