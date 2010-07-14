from file_project_creating_test_case import FileAndProjectCreatingTestCase
import json
import time
import roboide.controllers.vcs_bzr as bzr

class TestSyntaxChecker(FileAndProjectCreatingTestCase):
    valid_syntax_test_files = [
                                  "tests/resources/syntax/1.py",
                                  "tests/resources/syntax/2.py",
                                  "tests/resources/syntax/3.py"
                              ]

    invalid_syntax_test_files = [
                                    "tests/resources/syntax/4.py"
                                ]

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

    def asserted_valid_file(self, syntax_file_name, valid=True):
        projWrite = bzr.ProjectWrite(self.team, self.project_name, revno=self.rev)
        projWrite.update_file_contents("robot.py", open(syntax_file_name).read())
        projWrite.commit("update")
        code, dictionary = self.get_check_syntax_endpoint("robot.py")
        self.assertResponseCode200(code)

        if valid:
            self.assertEqual(int(dictionary["errors"]), 0, "file contained errors")
        else:
            self.assertNotEqual(int(dictionary["errors"]), 0, "file contained no errors")

        projWrite.destroy()
        self.rev += 1

    def test_valid_syntax(self):
        """
        Verifies the syntax of all the valid syntax files defined in this
        TestCase
        """

        for file in self.valid_syntax_test_files:
           self.asserted_valid_file(file)

    def test_invalid_file_syntax(self):
        """
        Verifies the (invalidness) syntax of all invalid syntax files defined
        in this TestCase
        """

        for file in self.invalid_syntax_test_files:
            self.asserted_valid_file(file, False)
