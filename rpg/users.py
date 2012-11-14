from flask import request
from rpg import app, password_hash
from rpg.database import User, errors
import httplib


@app.endpoint('/register', methods=['POST'])
#@app.route('/register', methods=['POST'])
def register():
    ''' register -> POST /register
        POST: username=[string]&password=[string]
    Tries to register the provided username with the provided password
    '''
    username = request.form['username']
    password = request.form['password']
    try:
        id = User.create({
            'username': username,
            'password': password_hash(password)
        })
    except errors.ExistingUsernameError:
        return httplib.CONFLICT

    return str(id), httplib.CREATED
