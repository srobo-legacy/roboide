# Standard imports
import unittest
import httplib
import json
import helpers
import os
import urllib

# TG imports
from turbogears import config

# SR imports
import roboide.vcs_bzr as vcs_bzr
import roboide.user as users

class TestEmptyProjectFunctions(unittest.TestCase):
    """
    Test an empty project.
    """

    def setUp(self):
        self.project_name = "testing-project"
        self.team = 1
        #open the teams repo
        self.repo_handle = vcs_bzr.open_repo(self.team)

        #create a project in the teams repo
        proj_url = users.get_repopath(self.team) + "/" + self.project_name
        self.repo_handle.bzrdir.create_branch_convenience(base=proj_url,force_new_tree=False)

        #connect to the server
        port = config.get('server.socket_port')
        host = config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)

        #call projlist (magically makes things work, hides internal bazaar fail)
        self.connection.request("GET", "/projlist?team=%s" % self.team)
        self.connection.getresponse()

    def tearDown(self):
        #undo the http connection
        self.connection.close()

        #delete the repo
        os.system("rm -rf %s/*" % (users.get_repopath(self.team).replace('file:///','/')))

    def get_create_file_endpoint(self, filename, filecontent, rev):
        """
        makes a request to the create file endpoint
        """

        params = urllib.urlencode({"code":filecontent})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        self.connection.request(
            "POST",
            "/savefile?team=%d&filepath=%s&rev=%d&message=%s" % (
                self.team,
                urllib.quote("/"+self.project_name+"/"+filename),
                rev,
                urllib.quote("testing message")
            ),
            params,
            headers
        )

        return self.connection.getresponse()

    def assertResponseCode200(self, code):
        """
        asserts that the passed response code is equal to 200
        """
        self.assertEqual(code, 200, "response code was not 200")

    def assertFileExistsInProject(self, filename):
        """
        asserts that the file exists in the project represented by this test
        """
        self.assertEqual(helpers.file_exists_in_project(filename, self.team, self.project_name), True, "created file does not exist")

    def test_create_files(self):
        """
        Test the creation of files.

        This test attmpts to create a collection of files in a project,
        and asserts their creation.
        """
        files = ["robot.py", "cows", "other.py"]

        #nb: this constant might need to be changed if the rcs in use ever changes
        rev = 0

        for file in files:
            response = self.get_create_file_endpoint(file, "empty", rev)
            self.assertResponseCode200(response.status)
            rev += 1
            self.assertFileExistsInProject(file)
