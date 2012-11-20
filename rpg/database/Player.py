from bson.objectid import ObjectId
from flask import url_for
from datetime import datetime
from . import collection, has_keys
from . import errors
database = collection("players")

player_keys = ["name"]


def __simple(packet):
    ''' __simple
    Returns the simple version of the Player document
    '''
    return {
        "name": packet["name"],
        "id": str(packet["_id"]),
        "age": str(datetime.utcnow() - packet["created"]),
        "url": url_for('get_player', player_id=str(packet["_id"]))
    }


def __complex(packet):
    ''' __complex
    Returns a more complex version of the Player document (versus __simple)
    '''
    return __simple(packet)


def create(info, user_id):
    ''' Player::create
    Used to create the player entry and store it in the database, the document
    passed in must include a specified set of keys (specified by `player_keys`,
    this is just a basic way of ensuring some consistency in a model.  Returns
    the player info and the id of the entry.
    '''
    if not has_keys(info, player_keys):
        raise errors.MissingInfoError(
            "Missing properties when creating a player.")

    info.update({
        'created': datetime.utcnow(),
        'created_by': ObjectId(user_id),
        'modified': None,
        'modified_by': None
    })

    id = database.insert(info)
    info['_id'] = id

    return __complex(info), str(id)


def get(info):
    ''' Player::get
    Retrieves a player document from the database based on the passed in
    packet.  The packet can either be the index or a dictionary of information
    to be used to filter, expects to only find one.
    '''
    if type(info) is unicode or type(info) is str:
        # if the argument is a string, treat like ObjectId
        info = ObjectId(info)

    player = database.find_one(info)
    if not player:
        raise errors.NoEntryError(
            "Information provided to find a Player document did not find " +
            "anything.")
    return __complex(player)


def all():
    ''' Player::all
    Retrieves *all* of the player documents from the database and returns a
    <list> of them.
    '''
    return [__simple(player) for player in database.find()]


def modify(info, user_id):
    ''' Player::modify
    Used on an existing player entry to modify/update the database document,
    used to save changes to the information for a player, such as name, exp,
    class, etc.
    '''
    if 'id' not in info:
        raise errors.NonMongoDocumentError(
            "Trying to modify a Player that is not in the database, use " +
            "Player::create instead.")

    info['_id'] = ObjectId(info['id'])
    del info['id']

    player = database.find_one(info['_id'])
    player.update(info)
    player.update({
        'modified': datetime.utcnow(),
        'modified_by': ObjectId(user_id)
    })

    return __complex(player) if database.save(player) else None
