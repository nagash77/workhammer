from bson.objectid import ObjectId
from flask import url_for
from datetime import datetime
from . import collection, has_keys
from . import errors
database = collection("quests")

quest_keys = ["name", "description", "rewards"]


def __simple(packet):
    ''' __simple
    Returns a simple version of the Quest document
    '''
    return {
        "name": packet["name"],
        "id": str(packet["_id"]),
        "description": packet["description"],
        "url": url_for("get_quest", quest_id=str(packet["_id"]))
    }


def __complex(packet):
    ''' __complex
    Returns a more complex version of the Quest document (versus __simple)
    '''
    return {
        "name": packet["name"],
        "id": str(packet["_id"]),
        "description": packet["description"],
        "url": url_for("get_quest", quest_id=str(packet["_id"])),
        "rewards": packet["rewards"]
    }


def create(info, user_id):
    ''' Quest::create
    Finishes creating the quest document (adds some built in pairs) and stores
    it in the database, the document passed in must include a set of keys (as
    specified in the `quest_keys` list, makes sure the quest model is
    consistent in some ways).  Returns the quest info and the id of the entry
    in the database.
    '''
    if not has_keys(info, quest_keys):
        raise errors.MissingInfoError(
            "Missing properties when creating a quest.")

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
    ''' Quest::get
    Retrieves a quest document from the database based on the argument.  The
    argument can either be an index of a document or a dictionary of
    information to filter with, expects only one document to be found.
    '''
    if type(info) is unicode or type(info) is str:
        # argument is a string, treat it like an ObjectId
        info = ObjectId(info)

    quest = database.find_one(info)
    if not quest:
        raise errors.NoEntryError(
            "Information provided to find a Quest document did not find " +
            "anything.")
    return __complex(quest)


def all():
    ''' Quest::all
    Returns a <list> of all of the available quests
    '''
    return [__simple(quest) for quest in database.find()]


def modify(info, user_id):
    ''' Quest::modify
    Used on an existing Quest, to modify/update the quest description in the
    database.
    '''
    if 'id' not in info:
        raise errors.NonMongoDocumentError(
            "Trying to modify a Quest that is not in the database, use " +
            "the Quest::create function instead.")

    info['_id'] = ObjectId(info['id'])
    del info['id']

    quest = database.find_one(info['_id'])
    quest.update(info)
    quest.update({
        'modified': datetime.utcnow(),
        'modified_by': ObjectId(user_id)
    })

    return __complex(quest) if database.save(quest) else None
