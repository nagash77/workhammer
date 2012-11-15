from bson.objectid import ObjectId
import rpg.database
database = rpg.database.collection("sessions")


def get(session_id):
    ''' Sessions::get
    Retrieves the session document from the database based on the index passed
    in.
    '''
    return database.find_one({"_id": ObjectId(session_id)})


def save(data):
    ''' Sessions::save
    Saves the passed in document to the database, performed as a safe operation
    so there should be no race conditions (the saving costs more time though).
    '''
    return database.save(data, safe=True)


def remove(session_id):
    ''' Sessions::remove
    Removes the passed in document from the database, used to perform a logout,
    the session will be invalidated, so make sure the session dictionary gets
    cleared.
    '''
    if type(session_id) is str:
        database.remove(ObjectId(session_id))
    else:
        database.remove(session_id)
