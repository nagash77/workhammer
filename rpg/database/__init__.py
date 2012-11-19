import pymongo as mongo
#import rpg.settings as settings
from .. import settings


connection_info = {
    'host': 'localhost',
    'port': 27017
}
connection_info.update(settings.MONGO_HOST)
connection = mongo.Connection(**connection_info)
if settings.DEBUG:
    database = connection.rpg_dev
else:
    database = connection.rpg


def cleanup():
    if settings.DEBUG:
        connection.drop_database("rpg_dev")


def collection(name):
    return database[name]


def has_keys(src, keys):
    ''' has_keys
    Checks that the <dict> src has all of the keys in keys
    '''
    return reduce(lambda a, b: a and b, map(lambda k: k in src, keys))
