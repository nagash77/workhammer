from bson.objectid import ObjectId
import rpg.database
database = rpg.database.collection("sessions")


def get(session_id):
    return database.find_one({"_id": ObjectId(session_id)})


def save(data):
    return database.save(data, safe=True)
