from file_project_creating_test_case import FileAndProjectCreatingTestCase
import json
import time

class TestSyntaxChecker(FileAndProjectCreatingTestCase):
    def get_check_syntax_endpoint(self, filename):
        self.connection.request("GET", "/checkcode?team=%d&path=%s&date=%d" % (
                self.team,
                "/" + self.project_name + "/" + filename,
                time.time()
            )
        )

        response = self.connection.getresponse()
        return response.status, json.loads(response.read())

    def test_default_file_syntax(self):
        code, dictionary = self.get_check_syntax_endpoint("robot.py")
        self.assertResponseCode200(code)
        self.assertEqual(int(dictionary["errors"]), 0, "file contained errors")
