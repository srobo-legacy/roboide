from file_project_creating_test_case import FileAndProjectCreatingTestCase
import json
import time
import roboide.vcs_bzr as bzr

class TestSyntaxChecker(FileAndProjectCreatingTestCase):
    test_files = ["tests/resources/syntax/1.py", "tests/resources/syntax/2.py", "tests/resources/syntax/3.py"]

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
        Tests that the default created test file contains no errors.
        """

        code, dictionary = self.get_check_syntax_endpoint("robot.py")
        self.assertResponseCode200(code)
        self.assertEqual(int(dictionary["errors"]), 0, "file contained errors")

    def asserted_valid_file(self, syntax_file_name):
        self.projWrite = bzr.ProjectWrite(self.team, self.project_name, revno=self.rev)
        self.projWrite.update_file_contents("robot.py", open(syntax_file_name).read())
        self.projWrite.commit("update")
        code, dictionary = self.get_check_syntax_endpoint("robot.py")
        self.assertResponseCode200(code)
        self.assertEqual(int(dictionary["errors"]), 0, "file contained errors")


    def test_control_flow_statements_syntax(self):
        """
        Verifies control statements (if, else, elif) with the syntax checker.
        """

        self.asserted_valid_file(self.test_files[0])

    def test_loop_statements_syntax(self):
        """
        Verifies loop statements (for, while) with the syntax checker.
        """

        self.asserted_valid_file(self.test_files[1])

    def test_sr_stuff_syntax(self):
        self.asserted_valid_file(self.test_files[1])
