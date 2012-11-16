''' decorators.py
This file defines the helper decorator functions, these are some application
wide decorators for routes to help with common tasks and scenarios for dealing
with the web requests.
'''
import json
from functools import wraps
from flask import request, make_response, Response, session, abort, \
    render_template, Flask
import httplib


def intersect(a, b):
    ''' intersect
    Returns a boolean if an item in <list> a is also in <list> b
    '''
    return reduce(lambda x, y: x or y, [i in a for i in b])


class RPGFlask(Flask):
    ''' RPGFlask:
    This is just an expansion on the Flask app class to add fancier decorators
    to the app
    '''
    def __init__(self, *args, **kwargs):
        self.endpoints = {}  # This is the storage property for the endpoints
        return Flask.__init__(self, *args, **kwargs)

    def endpoint(self, *args, **kwargs):
        ''' endpoing decorator:
        Like the route decorator, does the same thing except labels the route
        as an endpoint, meaning the route is a specific entry point into the
        application, other routes are given dynamically.
        '''
        def decorator(f):
            self.endpoints[f.__name__] = {
                'url': args[0]
            }
            return self.route(*args, **kwargs)(f)
        return decorator


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return json.JSONEncoder.default(self, obj)


JSON_KWARGS = {
    "cls": JSONEncoder,
    "separators": (',', ':')
}


def datatype(template=None):
    ''' datatype decorator:
    This decorator function is used to handle formatting and packaging a
    response coming out of a handler.  It will handle different scenarios and
    produce the proper format of output.  If the output of the route is a
    dictionary, it is assumed to be a data packet and will be formatted based
    on the HTTP Accept header, if it is a number, it is treated like a HTTP
    status code.

    argument(optional) template file to render html requests with

    ex:
        @datatype('some_function.html')
        @app.route('/some/path')
        def some_function():  # this will be converted into a proper response
            return { "foo": "bar" }
    '''
    mimetypes = {
        "application/json": lambda d: json.dumps(d, **JSON_KWARGS)
    }
    if type(template) is str:
        mimetypes["application/html"] = lambda d: \
            render_template(template, **d)
    default = 'application/json'

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            request.is_html = request.accept_mimetypes.accept_html
            data = func(*args, **kwargs)
            status_code = httplib.OK
            if type(data) is tuple:  # if multiple, break apart
                status_code = data[1]
                data = data[0]

            if type(data) is int:  # if int, treat it like a status code
                response = make_response("", data)
            elif type(data) is dict:  # if it is a dict, treat like data packet
                callback = request.args.get('callback', False)
                if callback:  # if has a callback parameter, treat like JSONP
                    data = str(callback) + "(" + \
                        mimetypes['application/json'](data) + ");"
                    response = make_response(data, status_code)
                    response.mimetype = 'application/javascript'
                else:  # Non-JSONP treatment
                    best = request.accept_mimetypes. \
                        best_match(mimetypes.keys())
                    data = mimetypes[best](data) if best \
                        else mimetypes[default](data)
                    response = make_response(data, status_code)
                    response.mimetype = best if best else default
            elif type(data) is Response:  # if it is a Response, already done
                response = data
            else:  # otherwise, treat it like raw data
                response = make_response(data, status_code)

            return response
        return decorated_function

    if hasattr(template, '__call__'):  # if no template was given
        return decorator(template)
    else:
        return decorator


def require_permissions(*roles):
    ''' require_permissions decorator:
    This decorator function is used to flag routes as endpoints that require
    the user to be logged in.  This is to easily take care of handling all of
    the checks on handlers that expect credentials to be in the session for
    the actions to be taken care of.

    ex:
        @require_permissions(roles.ADMIN)
        @app.route('/some/path')
        def some_function():  # Won't run if user is not an admin
            return { "foo": "bar" }
    '''
    from rpg import logger

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'id' not in session:
                logger.warn("Attempting to access without being logged in.")
                abort(httplib.UNAUTHORIZED)
            elif len(roles) and 'role' not in session \
                    and intersect(session['role'], roles):
                logger.warn("Attempting to access without sufficient " +
                            "permissions.  Has: {} Needs: {}",
                            session['role'], roles)
                abort(httplib.UNAUTHORIZED)
            return func(*args, **kwargs)
        return decorated_function

    if hasattr(roles[0], '__call__'):  # if no roles were given
        f = roles[0]
        roles = []
        return decorator(f)
    else:
        return decorator
