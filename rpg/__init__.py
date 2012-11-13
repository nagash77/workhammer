from database import connect
__version__ = "0.1"

database = connect()


def cleanup():
    ''' cleanup:
    Helper function used for testing, cleans up the app's database and
    environment during a testing.
    '''
    return

from flask import Flask
import rpg.session

app = Flask(__name__)
app.session_interface = rpg.session.Sessions(database)

if __name__ == '__main__':
    app.run()
