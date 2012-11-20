import unittest
import json
import httplib
import rpg


class TestBase(unittest.TestCase):
    ''' TestBase
    This is the base class for all tests, takes care of the setup and teardown
    of the tests and includes some nice helper methods for more specialized
    asserts
    '''

    json_header = [('Accept', 'application/json')]
    default_user = {
        "username": "TestUser",
        "password": "just a test password"
    }
    default_player = {
        "name": "TestPlayer"
    }

    def register(self, user=None):
        ''' TestBase::register
        Helper method, performs the basics of registering a user, takes a
        dictionary of the information for registering, if not provided, uses
        the TestBase::default_user packet.  Returns the response object.
        '''
        user = user if user else self.default_user
        return self.app.post(
            self.endpoints["register"]["url"], data=user,
            headers=self.json_header)

    def login(self, credentials=None):
        ''' TestBase::login
        Helper method, performs the basic login for a user using the provided
        credentials, returns the response.  If no credentials are provided,
        uses the TestBase::default_user set.
        '''
        credentials = credentials if credentials else self.default_user
        return self.app.post(
            self.endpoints["login"]["url"], data=credentials,
            headers=self.json_header)

    def logout(self):
        ''' TestBase::logout
        Helper method, performs a logout on the current user, returns whether
        the logout succeeded or not.
        '''
        response = self.app.get(
            self.endpoints["logout"]["url"],
            headers=self.json_header)
        return response.status_code == httplib.ACCEPTED

    def create_player(self, player=None):
        ''' TestBase::create_player
        Helper method, creates a player entry with the provided information.
        If no information provided, uses the self.player as default.
        '''
        player = player if player else self.default_player
        response = self.app.post(self.endpoints["players"]["url"],
                                 data=json.dumps(player),
                                 content_type="application/json",
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.CREATED)
        new_player = json.loads(response.data)
        self.assertEqual(player["name"], new_player["name"],
                         "Returned player's name is not the defined name.")
        return new_player

    def setUp(self):
        ''' TestBase::setUp
        set up method for the test suite, creates a test client for the Flask
        application and sets the application testing flag
        '''
        rpg.app.config['TESTING'] = True
        rpg.app.debug = False
        self.app = rpg.app.test_client()
        response = self.app.get('/', content_type="application/json")
        self.endpoints = json.loads(response.data)

    def tearDown(self):
        ''' TestBase::tearDown
        tear down method for the test suite
        '''
        rpg.cleanup()

    def assertEmpty(self, data, msg=None):
        ''' TestBase::assertEmpty
        wrapper for tests to check if a data set returned is empty, really is
        just used for readability
        '''
        self.assertEqual(len(data), 0, msg)

    def assertHasStatus(self, response, status, msg=None):
        ''' TestBase::assertHasStatus
        wrapper for tests to check if a response returns the correct HTTP
        status code
        params:
            response: <Response Object> returned from a test_client request
            status: <Int> for the expected status code or a <List> of the
                accepted status codes
            msg: <String> message to give to the assert call (default message
                is generated)
        '''
        if isinstance(status, list):
            if not msg:
                msg = "Response returned {} (expeded one of: {}) - {}".format(
                    response.status_code, str(status), response.data)
            self.assertIn(response.status_code, status, msg)
        else:
            if not msg:
                msg = "Response returned {} (expected: {}) - {}".format(
                    response.status_code, status, response.data)
            self.assertEqual(response.status_code, status, msg)
