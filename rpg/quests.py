''' quests.py
This is a collection of functions that handle the creation, modification, and
completion of quests.  The quests are tasks that are performed that give
rewards to the player characters.  They can be defined, modified/tweaked, and
completed by players.
'''
from flask import session, request
from . import app, filter_keys
from . import roles, logger
from .decorators import datatype, require_permissions
from .database import Quest, QuestLog, errors, Player
import httplib
# Keys that the user cannot directly change (controlled by app)
reserved_keys = []


@app.route("/quest", methods=["POST"])
@datatype
@require_permissions(roles.ROOT, roles.ADMIN)
def create_quest():
    ''' create_quest -> POST /quest
        POST: <JSON DATA>
    Submits a set of information to use in creating a quest
    '''
    if not request.json:
        return "POST body must be a JSON document for the quest to be made.", \
            httplib.BAD_REQUEST

    quest_info = request.json
    quest_info = filter_keys(quest_info, reserved_keys)

    try:
        info, id = Quest.create(quest_info, session["id"])
        logger.info("Quest %s (%s) was created by user %s.", info["name"],
                    id, session["id"])
    except errors.MissingInfoError as err:
        logger.info(err)
        return "Packet missing required keys", httplib.BAD_REQUEST

    return info, httplib.CREATED


@app.endpoint("/quest", methods=["GET"])
@datatype("quests.html")
def quests():
    ''' quests -> GET /quest
    Returns a <list> of all of the quests currently stored in the database
    '''
    return Quest.all()


@app.route("/quest/<quest_id>", methods=["GET"])
@datatype("quest.html")
def get_quest(quest_id):
    ''' get_quest -> GET /quest/<quest_id>
    Returns the full description of the quest specified by <quest_id>, this
    includes all completions of the quest.
    '''
    try:
        quest = Quest.get(quest_id)
        quest["completions"] = QuestLog.get(quest=quest_id)
    except errors.NoEntryError as err:
        logger.info(err)
        return "The given ID was not found for the Quest.", httplib.NOT_FOUND

    return quest


@app.route("/quest/<quest_id>", methods=["POST"])
@app.route("/player/<player_id>", methods=["POST"])
@datatype
@require_permissions(roles.ROOT, roles.ADMIN)
def complete_quest(player_id=None, quest_id=None):
    ''' complete_quest -> POST /quest/<quest_id>
            POST: player_id=[string]
        complete_quest -> POST /player/<player_id>
            POST: quest_id=[string]
    Stores that the specified player has completed the specified quest, will
    perform the updates to the Player based on the rewards of the completed
    quest.  This requires that the user performing this request has permissions
    to do so.
    '''
    player_id = request.form.get('player_id', player_id)
    quest_id = request.form.get('quest_id', quest_id)
    if not quest_id and not player_id:
        return "Need both the player and quest to mark the completion.", \
            httplib.BAD_REQUEST

    try:
        id, quest, player = QuestLog.add(quest_id, player_id, session['id'])
        apply_quest(quest, player)
        logger.info("%s (%s) completed %s (%s), reported by %s",
                    player["name"], player["id"], quest["name"], quest["id"],
                    session["id"])
        # Need to update the Player object now with the completed quest
    except errors.NoEntryError as err:
        logger.info(err)
        return "A given ID is not for an existing entry.", httplib.NOT_FOUND

    return httplib.ACCEPTED


def apply_quest(quest, player):
    ''' apply_quest
    Helper function, takes a quest object and a player object.  Loops through
    the rewards from the quest and applies them to the player (gives them).

    Reward types:
      <int> - added to the player property
      TODO: add more types (figure out what they should be)
    '''
    modifications = {"id": player["id"]}
    for (reward_type, reward)in quest["rewards"].items():
        if type(reward) is int:
            modifications[reward_type] = player[reward_type] + reward

    return Player.modify(modifications, session["id"])
