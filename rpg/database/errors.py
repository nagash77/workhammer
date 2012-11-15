class DatabaseError(Exception):
    ''' DatabaseError
    This is the base class for Database errors (this file defines them).  The
    base version takes parameters on creation that get fed into a string
    formatter and this gets returned as the string representation of the
    error.
    '''
    def __init__(self, *msg):
        self.message = msg[0].format(*msg[1:]) if len(msg) > 1 else msg[0]

    def __str__(self):
        return self.message


class ExistingUsernameError(DatabaseError):
    ''' ExistingUsernameError
    Raised when trying to create a User (register) with a username that is
    already taken, causing a collision.
    '''
    pass


class MissingInfoError(DatabaseError):
    ''' MissingInfoError
    Raised when an operation on the database is performed without the necessary
    information.
    '''
    pass
