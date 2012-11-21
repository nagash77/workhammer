from base import TestBase
#from unittest import skip
import json
import httplib


class QuestTest(TestBase):
    ''' QuestTest
    Test suite to test the question system, including creating quest(s) and
    players completing the quest(s).
    '''

    player = {
        "name": "Megatron"
    }

    root_user = {
        "username": "dungeon_master",
        "password": "blah blah password security"
    }

    quest = {
        "name": "Test Quest",
        "description": "Just a quest for testing",
        "rewards": {
            "experience": 5
        }
    }

    def setUp(self):
        ''' QuestTest::setUp
        Overloaded setup call, this is responsible for creating a root user by
        default.  Mostly useful because of the requirement of a DM user for
        most of the tests.
        '''
        TestBase.setUp(self)
        self.register(self.root_user)

    def create_quest(self, quest=None):
        ''' QuestTest::create_quest
        '''
        quest = quest if quest else self.quest
        response = self.app.post(self.endpoints["quests"]["url"],
                                 data=json.dumps(quest),
                                 content_type="application/json",
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.CREATED)
        new_quest = json.loads(response.data)
        return new_quest

    def get_quest_list(self):
        ''' QuestTest::get_quest_list
        '''
        response = self.app.get(self.endpoints["quests"]["url"],
                                headers=self.json_header)
        self.assertHasStatus(response, httplib.OK)
        return json.loads(response.data)

    def test_create_basic_quest(self):
        ''' Tests creating just a basic quest
        Creates a basic quest (just rewards basic experience).
        '''
        quest = self.create_quest()
        response = self.app.get(quest["url"],
                                headers=self.json_header)
        self.assertHasStatus(response, httplib.OK)

        quests = self.get_quest_list()
        self.assertEqual(1, len(quests))

    def test_apply_basic_quest(self):
        ''' Test creating a basic quest and applying it
        Creates a basic quest, then creates a new player and has the player
        complete this quest.  Makes sure the rewards of the quest get applied.
        '''
        self.assertTrue(self.logout(), "Logout failed.")

        response = self.register({
            "username": "Quester",
            "password": "QuestAretehKewlest"
        })
        self.assertHasStatus(response, httplib.CREATED)
        player = self.create_player(self.player)
        self.assertTrue(self.logout(), "Logout failed.")

        self.assertHasStatus(self.login(self.root_user), httplib.OK)

        quest = self.create_quest()
        # complete quest with the quest URL as the access point
        response = self.app.post(quest["url"],
                                 data={"player_id": player['id']},
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.ACCEPTED)
        # complete quest with the player URL as the access point
        response = self.app.post(player["url"],
                                 data={"quest_id": quest['id']},
                                 headers=self.json_header)
        self.assertHasStatus(response, httplib.ACCEPTED)

        response = self.app.get(player["url"] + "?quests",
                                headers=self.json_header)
        self.assertHasStatus(response, httplib.OK)
        player = json.loads(response.data)
        self.assertEqual(player['experience'],
                         self.quest["rewards"]["experience"] * 2,
                         "Experience not updated for player.")
        self.assertEqual(len(player['quests']), 2,
                         "Quests list does not have all of the completed " +
                         "quests in it.")
