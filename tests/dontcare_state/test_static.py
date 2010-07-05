import unittest
import httplib

from turbogears import config

import os

class StaticFilesTest(unittest.TestCase):
    """
    Tests that static files are available.
    """

    def setUp(self):
        port = config.get('server.socket_port')
        host = config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)
        self.files = []
        os.path.walk("roboide/static/", self.buildfiles, "")

    def buildfiles(self, arg, path, names):
        """
        Build the list of static files.
        """

        for name in names:
            path = path.replace("roboide", "")
            if path[-1] != os.path.sep:
                path += os.path.sep
            self.files.append(path + name)

    def tearDown(self):
        self.connection.close()

    def test_static_files(self):
        """
        Tests the presence of static files, based on the list built up
        from /roboide/static.
        """

        for file in self.files:
            if file.find(".") != -1:
                self.connection.request("GET", file)
                response = self.connection.getresponse()
                self.assertEqual(response.status, 200, "response code on static file was not 200")

    def test_static_home_page(self):
        """
        Tests that the homepage is available.
        """

        self.connection.request("GET", "/")
        response = self.connection.getresponse()
        self.assertEqual(response.status, 200, "response code on home page was not 200")
