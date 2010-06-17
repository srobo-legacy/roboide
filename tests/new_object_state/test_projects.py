
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
    def setUp(self):
        port =  config.get('server.socket_port')
        host =  config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)

    def tearDown(self):
        self.connection.close()
        for i in range(0,2):
            os.system("rm -rf %s/*" % get_repopath(i).replace('file:///','/'))


    def test_create_project(self):
        proj = 'new-project'
        team = 1
        self.connection.request("GET", "/projlist?team=%s" % team)
        r = self.connection.getresponse().read()
        p = json.loads(r)['projects']
        self.assertEqual(p, [], "projects present before first creation")

        self.connection.request("GET", "/createproj?name=%s&team=%s" % (proj, team))
        response = self.connection.getresponse()
        print response.read()
        self.assertEqual(helpers.does_project_exist(team, proj), True, "created project did not exist")

