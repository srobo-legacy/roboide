import unittest
import httplib
import os

from helpers.confighelper import global_config_helper

class StaticFilesTest(unittest.TestCase):
    """
    Tests that static files are available.
    """

    def setUp(self):
        port = global_config_helper.get('server:main.port')
        host = global_config_helper.get('server:main.host')
        self.connection = httplib.HTTPConnection(host, port)
        self.files = []
        os.path.walk("roboide/public/", self.buildfiles, "")

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
        from /roboide/public.
        """

        for file in self.files:
            if file.find(".") != -1:
                self.connection.request("GET", file.replace("/public", ""))
                response = self.connection.getresponse()
                self.assertEqual(response.status, 200, "response code on static file was not 200")
                f = open("roboide" + file)
                self.assertEqual(f.read(), response.read(), "response file was not same as file on filesystem")

    def test_static_home_page(self):
        """
        Tests that the homepage is available.
        """

        self.connection.request("GET", "/")
        response = self.connection.getresponse()
        self.assertEqual(response.status, 200, "response code on home page was not 200")
