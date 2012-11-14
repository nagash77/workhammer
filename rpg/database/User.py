import rpg.database
from rpg.database import errors
database = rpg.database.collection("users")


def create(info=None):
    ''' User.create
    Tries to create an entry in the users table with the provided credentials,
    returns the user ID.
    '''
    if database.find_one({"username": info["username"]}):
        raise errors.ExistingUsernameError('Username: %s already exists',
                info["username"])
    return database.insert(info)
