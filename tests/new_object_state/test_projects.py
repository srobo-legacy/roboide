
# Standard imports
import unittest
import httplib
import json
import helpers
import os

# TurboGears imports
from turbogears import config

# roboide imports
from roboide.user import get_repopath

class TestProjectFunctions(unittest.TestCase):
    """
    Test an empty repo.
    """

    def setUp(self):
        port = config.get('server.socket_port')
        host = config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)

    def tearDown(self):
        self.connection.close()
        for i in range(0,2):
            os.system("rm -rf %s/*" % get_repopath(i).replace('file:///','/'))


    def test_create_project(self):
        """
        Test the creation of projects.

        This test attmpts to create a project, and assert this creation.
        """

        projects = 'new-project','potatoes'
        teams = [1,2]

        for team in teams:
            self.connection.request("GET", "/projlist?team=%s" % team)
            r = self.connection.getresponse().read()
            p = json.loads(r)['projects']
            self.assertEqual(p, [], "projects present before first creation")

        for proj in projects:
            for team in teams:
                self.connection.request("GET", "/createproj?name=%s&team=%s" % (proj, team))
                response = self.connection.getresponse()
                self.assertEqual(helpers.does_project_exist(team, proj), True, "created project did not exist")
