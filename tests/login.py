from base import TestBase
from unittest import skip
import json
import httplib


class LoginTest(TestBase):
    ''' LoginTest
    Test suite to test the login functionality.
    '''
    user = {
        "username": "testuser",
        "password": "testting password"
    }

    def register(self, user=None):
        ''' LoginTest::register
        Helper method, performs the basics of registering a user, takes a
        dictionary of the credentials to use, if not provided, the class
        default credentials are used.
        '''
        user = user if user else self.user
        response = self.app.post('/register', data=user)
        return response.data, response

    def test_good_login(self):
        ''' LoginTest::test_good_login
        Performs a login that should be successful, base test (if this fails,
        most of the subsequent tests in this suite should fail).
        '''
        self.assertTrue(True)

    def test_bad_login(self):
        ''' LoginTest::test_bad_login
        Performs a login that should fail, used to make sure the failure
        reporting and response are properly working.
        '''
        self.assertTrue(True)

    @skip("Reset password functionality will be added later")
    def test_reset_password(self):
        ''' LoginTest::test_reset_password
        Requests a password reset, this should then kick off the process to
        recover an account with a forgotten password.
        '''
        self.skipTest("Test not written yet")

    def test_register(self):
        ''' LoginTest::test_register
        Registers a new user, should go through the full process to create the
        user and then make sure the user has logged in.
        '''
        user_id, response = self.register()
        self.assertHasStatus(response, httplib.CREATED)
