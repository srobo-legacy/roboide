# Standard imports
import unittest
import httplib
import helpers
import os
import urllib

# TG imports
from turbogears import config

# SR imports
import roboide.vcs_bzr as vcs_bzr
import roboide.user as users

class ProjectCreatingTestCase(unittest.TestCase):
    def setUp(self):
        self.project_name = "testing-project"
        self.team = 1
        #open the team repo
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

        #handle revision at the class level
        self.rev = 0

    def tearDown(self):
        #undo the http connection
        self.connection.close()

        #delete the repo
        os.system("rm -rf %s/*" % (users.get_repopath(self.team).replace('file:///','/')))

        #reset revision back to 0
        self.rev = 0

    def get_save_file_endpoint(self, filename, filecontent, rev, commit_message="testing message"):
        """
        Makes a request to the save file endpoint.

        will create a file if it does not already exist
        """

        params = urllib.urlencode({"code":filecontent})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        self.connection.request(
            "POST",
            "/savefile?team=%d&filepath=%s&rev=%d&message=%s" % (
                self.team,
                urllib.quote("/"+self.project_name+"/"+filename),
                rev,
                urllib.quote(commit_message)
            ),
            params,
            headers
        )

        return self.connection.getresponse()

    def get_delete_file_endpoint(self, filename):
        """
        Makes a request to the delete file endpoint.
        """

        self.connection.request(
            "GET",
            "/delete?team=%d&project=%s&files=%s&kind=ALL" %
            (
                self.team,
                urllib.quote(self.project_name),
                urllib.quote(filename)
            )
        )

        response = self.connection.getresponse()

    def assertResponseCode200(self, code):
        """
        Asserts that the passed response code is equal to 200.
        """

        self.assertEqual(code, 200, "response code was not 200")

    def assertFileExistsInProject(self, filename):
        """
        Asserts that the file exists in the project represented by this test.
        """

        self.assertEqual(helpers.file_exists_in_project(filename, self.team, self.project_name), True, "created file does not exist")

    def assertFileDoesNotExistInProject(self, filename):
        """
        Asserts that a file does not exist in the project represented by this test.
        """

        self.assertEqual(helpers.file_exists_in_project(filename, self.team, self.project_name), False, "deleted file exists")

    def asserted_create_file(self, filename, contents, message="testing create"):
        """
        Creates a file whilst making assertions.

        pre-asserts the file doesn't exist, post asserts that the file exists
        and that the response code from the http server was 200
        """

        self.assertFileDoesNotExistInProject(filename)
        response = self.get_save_file_endpoint(filename, contents, self.rev, message)
        self.rev += 1
        self.assertFileExistsInProject(filename)
        self.assertResponseCode200(response.status)

    def asserted_modify_file(self, filename, contents, message="testing modify"):
        """
        Modify a file whilst making assertions.

        pre-asserts the file exists, post asserts that the file has the new content
        and that the response code from the http server was 200
        """

        self.assertFileExistsInProject(filename)
        response = self.get_save_file_endpoint(filename, contents, self.rev, message)
        self.rev += 1
        actual_file_contents = helpers.get_file_contents(filename, self.team, self.project_name)
        self.assertEqual(actual_file_contents,
                         contents,
                         "file did not match expected contents \"%s\" actual contents were \"%s\"" % (contents, actual_file_contents))
        self.assertResponseCode200(response.status)

    def asserted_create_files(self, files):
        """
        Creates files with the filenames passed in the files list, asserting
        that they were created successfully.
        """

        #nb: this constant might need to be changed if the rcs in use ever changes
        rev = 0

        for file in files:
            self.asserted_create_file(file, "empty")

    def asserted_delete_file(self, filename):
        """
        Deletes a file and asserts it has been deleted
        """

        self.get_delete_file_endpoint(filename)
        self.assertFileDoesNotExistInProject(filename)


