''' html.py
This is the collection of functions serving simple HTML pages that will be
loaded, most of these are static endpoints that are basically a minimal
fallback from dynamically creating the markup for the pages.  This can
probably be left out of any advanced application or API usage.
'''
from rpg import app
from rpg.decorators import datatype


@app.route('/register', methods=['GET'])
@datatype("register.html")
def register_page():
    return {}


@app.route('/login', methods=['GET'])
@datatype("login.html")
def login_page():
    return {}