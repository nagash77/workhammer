import json
from functools import wraps
from flask import request, make_response, Response, session, abort, \
        render_template
import httplib


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
            data = func(*args, **kwargs)
            if type(data) is tuple:  # if multiple, treat normally
                response = make_response(*data)
            elif type(data) is int:  # if int, treat it like a status code
                response = make_response("", data)
            elif type(data) is dict:  # if it is a dict, treat like data packet
                callback = request.args.get('callback', False)
                if callback:  # if has a callback parameter, treat like JSONP
                    data = str(callback) + "(" + \
                            mimetypes['application/json'](data) + ");"
                    response = make_response(data)
                    response.mimetype = 'application/javascript'
                else:  # Non-JSONP treatment
                    best = request.accept_mimetypes. \
                            best_match(mimetypes.keys())
                    data = mimetypes[best](data) if best \
                            else mimetypes[default](data)
                    response = make_response(data)
                    response.mimetype = best if best else default
            elif type(data) is Response:  # if it is a Response, already done
                response = data
            else:  # otherwise, treat it like raw data
                response = make_response(data)

            return response
        return decorated_function

    if hasattr(template, '__call__'):  # if no template was given
        return decorator(template)
    else:
        return decorator


def require_credentials(func):
    ''' require_credentials decorator:
    This decorator function is used to flag routes as endpoints that require
    the user to be logged in.  This is to easily take care of handling all of
    the checks on handlers that expect credentials to be in the session for
    the actions to be taken care of.

    ex:
        @require_credentials
        @app.route('/some/path')
        def some_function():  # this will only be run if the user is logged in
            return { "foo": "bar" }
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:  # is this correct?
            abort(httplib.UNAUTHORIZED)
        return func(*args, **kwargs)
