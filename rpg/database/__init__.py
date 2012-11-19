import pymongo as mongo
import rpg.settings as settings


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
