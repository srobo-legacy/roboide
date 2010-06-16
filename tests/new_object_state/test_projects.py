import unittest
import httplib
import json
import helpers
import os

class TestProjectFunctions(unittest.TestCase):
    def setUp(self):
        self.connection = httplib.HTTPConnection("localhost:8080")

    def tearDown(self):
        self.connection.close()
        os.system("rm -rf ../repos/1/*")
        os.system("rm -rf ../repos/2/*")


    def test_create_project(self):
        self.connection.request("GET", "http://localhost:8080/createproj?name=new-project&team=1")
        response = self.connection.getresponse()
        print response.read()
        self.assertEqual(helpers.does_project_exist(1, "new-project"), True, "created project did not exist")

