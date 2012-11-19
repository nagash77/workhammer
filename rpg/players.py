''' players.py
This is the collection of functions that handle the creation and modification
of the player constructs.  The player constructs are the identifying structures
through the web app (versus users which is the authentication construct).
'''
from flask import request, redirect, url_for, session
from bson.objectid import ObjectId
from rpg import app, roles, logger
from rpg.database import Player, errors, User
from rpg.decorators import datatype, require_permissions, intersect
import httplib
# Keys that the user cannot directly change (controlled by app)
reserved_keys = ["experience"]


def filter_keys(src, blacklist):
    ''' filter_keys
    Helper function, removes the (key, value) pairs for keys in the blacklist
    list, returns filtered dictionary.
    '''
    for key in blacklist:
        if key in src:
            del src[key]

    return src


@app.route("/player", methods=["POST"])
@datatype
@require_permissions
def create_player():
    ''' create_player -> POST /player
        POST: <JSON DATA>
    Submits a set of player information to use in creating a player, this can
    be creating a player for another user or for the current user if:
        * the current user is ADMIN or ROOT, can create for another user
        * the current user is PLAYER (meaning does not have own player),
          creates for the current user
    '''
    if not request.json:
        return "POST body must be a JSON document for the player to be " +\
            "made.", \
            httplib.BAD_REQUEST

    player_info = request.json
    if "user" in player_info and player_info["user"] != session["id"]:
        if not intersect(session["role"], [roles.ADMIN, roles.ROOT]):
            return "You do not have permissions to create a player for " + \
                   "another user.", httplib.UNAUTHORIZED
        target_user = User.lookup(id=player_info["user"])
        if not target_user:
            return "Targetted user does not exist", httplib.NOT_FOUND
        elif "PLAYER" in target_user["role"]:
            return "User already has a player", httplib.CONFLICT
    elif roles.PLAYER in session["role"] and "player" in session:
        return "User already has a player.", httplib.CONFLICT
    else:
        player_info["user"] = session["id"]

    player_info = filter_keys(player_info, reserved_keys)

    try:
        info, id = Player.create(player_info, session['id'])
        logger.info("Player %s (%s) was created for user %s.", info["name"],
                    info["id"], session["id"])
        if player_info["user"] == session["id"]:  # update session
            session["player"] = id
            session["role"] = session["role"] + [roles.PLAYER]

        User.modify({  # This adds the PLAYER role to the user
            "role": session["role"] + [roles.PLAYER],
            "id": player_info["user"],
            "player": ObjectId(id)
        }, session["id"])
    except errors.MissingInfoError as err:
        logger.info(err)
        return "Packet missing required keys", httplib.BAD_REQUEST

    return redirect(url_for('get_player', player_id=id)) \
        if request.is_html else (info, httplib.CREATED)


@app.endpoint("/player", methods=["GET"])
@datatype("players.html")
def players():
    ''' players -> GET /player
    Returns an array of the players
    '''
    return Player.all()


@app.route("/player/<player_id>", methods=["GET"])
@datatype("player.html")
def get_player(player_id):
    ''' get_player -> GET /player/<id>
    Using the provided <id>, returns the specified player or NOT_FOUND if the
    <id> does not match any stored player.
    '''
    try:
        player = Player.get(player_id)
    except errors.NoEntryError as err:
        logger.info(err)
        return "No player corresponds to this url.", httplib.NOT_FOUND

    return player


@app.route("/player/<player_id>", methods=["POST"])
@datatype
@require_permissions
def modify_player(player_id):
    ''' modify_player -> POST /player/<id>
        POST: <JSON DATA>
    Uses the POSTed JSON data to update the player specified by <id>, will
    throw a NOT_FOUND if the <id> does not match any stored player.
    '''
    if not request.json:
        return httplib.BAD_REQUEST

    player_info = request.json
    player_info['id'] = player_id

    try:
        player_info = Player.modify(player_info, session['id'])
        if not player_info:
            return httplib.BAD_REQUEST
    except errors.NonMongoDocumentError as err:
        logger.info(err)
        return "Trying to modify a non existent player", httplib.BAD_REQUEST

    return redirect(url_for('get_player', player_id=player_id)) \
        if request.is_html else (player_info, httplib.ACCEPTED)
