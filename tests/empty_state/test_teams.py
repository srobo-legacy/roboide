import unittest
import httplib
import json
import helpers
from turbogears import config

class TestTeamFunctions(unittest.TestCase):
    def setUp(self):
        port =  config.get('server.socket_port')
        host =  config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)

    def tearDown(self):
        self.connection.close()

    def test_team_membership(self):
        self.connection.request("GET", "/user/info")
        response = self.connection.getresponse()
        response_object = json.loads(response.read())
        teams_dictionary = response_object["teams"]
        expected_teams_dictionary = helpers.get_team_dictionary()
        for key in response_object["teams"]:
            self.assertEqual(expected_teams_dictionary.has_key(int(key)), True, "Team not found in expected")
            self.assertEqual(expected_teams_dictionary[int(key)], teams_dictionary[key], "Team name not equal to value in expected")

