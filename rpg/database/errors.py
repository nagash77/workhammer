class ExistingUsernameError(Exception):
    ''' ExistingUsernameError
    Raised when trying to create a User (register) with a username that is
    already taken, causing a collision.
    '''
    pass
