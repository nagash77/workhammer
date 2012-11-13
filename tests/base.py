import unittest
import rpg


class TestBase(unittest.TestCase):
    ''' TestBase
    This is the base class for all tests, takes care of the setup and teardown
    of the tests and includes some nice helper methods for more specialized
    asserts
    '''

    def setUp(self):
        ''' TestBase::setUp
        set up method for the test suite, creates a test client for the Flask
        application and sets the application testing flag
        '''
        rpg.app.config['TESTING'] = True
        self.app = rpg.app.test_client()

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
                msg = "Response returned {} (expeded one of: {})".format(
                    response.status_code, str(status))
            self.assertIn(response.status_code, status, msg)
        else:
            if not msg:
                msg = "Response returned {} (expected: {})".format(
                    response.status_code, status)
            self.assertEqual(response.status_code, status, msg)
