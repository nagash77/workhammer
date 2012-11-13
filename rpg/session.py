from flask.sessions import SessionInterface, SessionMixin
from settings import settings

SESSION_KEY = settings.get('session_key', 'session_key')


class Session(dict, SessionMixin):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self["permissions"] = []
        #self.update(settings.get('session_defaults', {}))

    pass


class Sessions(SessionInterface):
    ''' Sessions
    class implementing the SessionInterface for Flask to store the sessions in
    the database, this could always use plenty of work.
    '''
    def __init__(self, db):
        self.db = db

    def open_session(self, app, request):
        ''' Sessions::open_session
        if no key is stored in the cookies, returns None, otherwise will return
        the data packet stored in the database using the key retrieved from the
        cookie.
        '''
        if SESSION_KEY not in request.cookies:
            return Session()
        session = self.db.Session.get(request.cookies[SESSION_KEY])
        return session if session else Session()

    def save_session(self, app, session, response):
        ''' Sessions::save_session
        saves the session packet into the database and checks if this is a new
        session packet or not (if the is an id in the packet), if it is new,
        the id will be stored as a cookie for future lookup
        '''
        id = self.db.Session.save(session)
        response.set_cookie(SESSION_KEY, value=id)
