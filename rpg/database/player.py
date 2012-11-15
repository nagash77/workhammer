import rpg.database
from rpg.database import errors
database = rpg.database.collection("players")

player_keys = ["name"]


def has_keys(src, keys):
    ''' has_keys
    Checks that the <dict> src has all of the keys in keys
    '''
    return reduce(lambda a, b: a and b, map(lambda k: k in src, keys))


def create(info):
    ''' Player.create
    '''
    if not has_keys(info, player_keys):
        raise errors.MissingInfoError("Missing properties when creating a " + \
                "player.")

    return info
