from bson.objectid import ObjectId
from datetime import datetime
import rpg.database
from rpg.database import errors
from rpg import roles
database = rpg.database.collection("users")

default_role = roles.PLAYER


def __private_user(packet):
    ''' __private_user
    Helper function, takes the raw mongo user document and returns only the
    whitelisted (key, value) pairs that the user should see
    '''
    return {
        "username": packet["username"],
        "id": str(packet["_id"]),
        "role": packet["role"]
    }


def __public_user(packet):
    ''' __public_user
    Helper function, takes the raw mongo user document and returns only the
    whitelisted (key, value) pairs that should be publicly visible
    '''
    return {
        "username": packet["username"]
    }


def create(info, role=[default_role]):
    ''' User.create
    Tries to create an entry in the users table with the provided credentials,
    returns the user ID.
    '''
    if database.find_one({"username": info["username"]}):
        raise errors.ExistingUsernameError('Username: %s already exists',
                info["username"])

    if type(role) is not list:
        role = [role]

    if database.count() == 0:
        role.append(roles.ROOT)

    info.update({
        'role': role,
        'created': datetime.utcnow(),
        'modified': None,
        'modified_by': None
    })

    id = database.insert(info)

    return id, role


def modify(info, user_id):
    ''' User.modify
    Takes a user packet and the current user's ID and updates the user packet
    in the database, the user's ID is used to note who modified the user.
    '''
    info.update({
        'modified': datetime.utcnow(),
        'modified_by': ObjectId(user_id)
    })
    return database.save(info)


def login(username, pwhash):
    ''' User.login
    Tries to retrieve the user from the database using the provided credentials
    and returns the user's info packet and their private ID (used for with the
    session).  If it fails, the ID will be None.
    '''
    user = database.find_one({"username": username, "password": pwhash})
    return (__private_user(user), user['_id']) if user else (None, None)


def lookup(username=None, id=None):
    ''' User.lookup
    Retrieves the user info from the database using the provided identity
    information.  Takes either the user's ID or username, returns None if no
    User was found, otherwise returns the public packet.
    '''
    packet = {}
    if username:
        packet["username"] = username
    if id:
        packet["_id"] = ObjectId(id)

    user = database.find_one(packet)
    if user:
        user = __public_user(user)

    return user
