# Standard imports
import os

# TG imports
from turbogears import config

# Test imports
import helpers
from tests.project_creating_test_case import ProjectCreatingTestCase

class TestEmptyProjectFunctions(ProjectCreatingTestCase):
    """
    Test an empty project.
    """

    def test_empty_file_list(self):
        """
        Test that the freshly commited project is empty.
        """

        helpers.checkout_repository(self.team, self.project_name, "/tmp/repo")
        files = os.listdir("/tmp/repo")
        visible_files = []

        for file in files:
            if file[0] != '.':
                visible_files.append(file)

        self.assertEqual(visible_files, [], "files were in the repo")

    def test_create_files(self):
        """
        Test the creation of files.

        This test attmpts to create a collection of files in a project,
        and asserts their creation.
        """

        files = ["robot.py", "cows", "other.py"]
        self.asserted_create_files(files)

    def test_create_delete_files(self):
        """
        Tests the creation and gradual deletion of a bunch of files.

        note: no robot.py is created in this test
        """

        files = ["cows.py", "cheese", "monkeys.py"]
        self.asserted_create_files(files)
        for i in range(0, len(files)):
            self.asserted_delete_file(files[i])
            for remaining_file in files[i+1:]:
                self.assertFileExistsInProject(remaining_file)

    def test_create_modify_files(self):
        """
        Tests the creation of a file with some content and modifying it.
        """

        files = ["robot.py", "bees.py", "cows"]
        self.asserted_create_files(files)
        iterations = ["massive amounts of ponies", "cheese", "bacons"]
        for iteration in iterations:
            for file in files:
                self.asserted_modify_file(file, iteration)
