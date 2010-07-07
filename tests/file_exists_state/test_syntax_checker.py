from file_project_creating_test_case import FileAndProjectCreatingTestCase
import json
import time

class TestSyntaxChecker(FileAndProjectCreatingTestCase):
    test_files = ["tests/resources/syntax/1.py"]

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
        """
        Tests that the default created test file contains no errors
        """

        code, dictionary = self.get_check_syntax_endpoint("robot.py")
        self.assertResponseCode200(code)
        self.assertEqual(int(dictionary["errors"]), 0, "file contained errors")

    def test_control_flow_statements_syntax(self):
        self.projWrite.update_file_contents("robot.py", open(self.test_files[0]).read())
