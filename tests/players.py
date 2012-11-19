from base import TestBase
import json
import httplib


class PlayerTest(TestBase):
    ''' PlayerTest
    Test suite to test the player information functionality.
    '''

    player = {
        "name": "Trogdor"
    }

    root_user = {
        "username": "rootuser",
        "password": "i am teh rootz0rz"
    }

    def setUp(self):
        ''' PlayerTest::setUp
        Overloaded setup call, This is responsible for creating a root user by
        default and logging them out.  Mostly useful because all of the users
        created subsequently will have default permissions.
        '''
        TestBase.setUp(self)
        self.register(self.root_user)
        self.logout()

    def create_player(self, player=None):
        ''' PlayerTest::create_player
        Helper method, creates a player entry with the provided information.
        If no information provided, uses the self.player as default.
        '''
        player = player if player else self.player
        response = self.app.post(self.endpoints["players"]["url"],
                                 data=json.dumps(player),
                                 content_type="application/json",
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.CREATED)
        new_player = json.loads(response.data)
        self.assertEqual(player["name"], new_player["name"],
                         "Returned player's name is not the defined name.")
        return new_player

    def get_player_list(self):
        ''' PlayerTest::get_player_list
        Helper method, retrieves the list of players.  Checks the request was
        successful and returns a <list> of the player entries.
        '''
        response = self.app.get(self.endpoints["players"]["url"],
                                headers=self.json_header)
        self.assertHasStatus(response, httplib.OK)
        return json.loads(response.data)

    def test_empty_list(self):
        ''' Test empty player list
        Grabs the player list (which should be initially empty) and makes sure
        it returns an empty array.
        '''
        players = self.get_player_list()
        self.assertEmpty(players, "Returned player list was not empty.")

    def test_create_own_player(self):
        ''' Test a user creating their own player
        Creates a player for current user, then checks to see that the player
        was properly created.
        '''
        response = self.register()
        self.assertHasStatus(response, httplib.CREATED)

        player = self.create_player()
        self.assertIn("url", player)

        players = self.get_player_list()
        self.assertEqual(
            1, len(players),
            "The returned player list " +
            "({}) is not the expected size (1)".format(len(players)))

        response = self.app.get(player["url"], headers=self.json_header)
        self.assertHasStatus(response, httplib.OK)
        data = json.loads(response.data)
        self.assertEqual(data["name"], player["name"])

    def test_create_other_player(self):
        ''' Test a DM creating a player for another user
        Creates a player for another user, then checks that the player was
        properly created.
        '''
        response = self.register()
        self.assertHasStatus(response, httplib.CREATED)
        id = response.data
        self.assertTrue(self.logout(), "Logout failed.")

        response = self.login(self.root_user)
        self.assertHasStatus(response, httplib.OK)

        other_player = {'user': id}
        other_player.update(self.player)
        self.create_player(other_player)
        self.create_player(self.player)

    def test_edit_player(self):
        ''' Test a user editting their player
        Creates a player, then modifies the player.  The player's data should
        be changed and not create a new clone.
        '''
        response = self.register()
        self.assertHasStatus(response, httplib.CREATED)
        player_orig = self.create_player({
            "name": "Charles"
        })

        new_name = "Chuck"
        response = self.app.post(
            player_orig["url"],
            data=json.dumps({"name": new_name}),
            content_type="application/json",
            headers=self.json_header)
        self.assertHasStatus(response, httplib.ACCEPTED)
        player_new = json.loads(response.data)

        self.assertEqual(
            new_name, player_new["name"],
            "Player's name was not properly changed ({} - {})".format(
                new_name, player_new["name"]))
        self.assertEqual(
            player_orig["url"], player_new["url"],
            "Player URL was changed: {} -> {}".format(
                player_orig["url"], player_new["url"]))

        players = self.get_player_list()
        self.assertEqual(
            1, len(players),
            "The returned player list " +
            "({}) is not the expected size (1)".format(len(players)))

    def test_create_second_player(self):
        ''' Test a player trying to create a second player
        Tries to create a player for a user that already has one, should fail
        with a warning of this condition.
        '''
        response = self.register()
        self.assertHasStatus(response, httplib.CREATED)
        self.create_player()

        response = self.app.post(self.endpoints["players"]["url"],
                                 data=json.dumps(self.player),
                                 content_type="application/json",
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.CONFLICT)
