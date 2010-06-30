import unittest
import httplib

from turbogears import config

import os

class StaticFilesTest(unittest.TestCase):
    """
    tests that static files are available
    """
    def setUp(self):
        port = config.get('server.socket_port')
        host = config.get('server.socket_host')
        self.connection = httplib.HTTPConnection(host, port)
        self.files = []
        os.path.walk("roboide/static/", self.buildfiles, "")

    def buildfiles(self, arg, path, names):
        for name in names:
            path = path.replace("roboide", "")
            if path[-1] != os.path.sep:
                path += os.path.sep
            self.files.append(path + name)

    def tearDown(self):
        self.connection.close()

    def test_static_files(self):
        for file in self.files:
            if file.find(".") != -1:
                self.connection.request("GET", file)
                response = self.connection.getresponse()
                self.assertEqual(response.status, 200, "response code on static file was not 200")
