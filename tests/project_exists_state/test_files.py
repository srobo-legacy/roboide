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
from project_creating_test_case import ProjectCreatingTestCase

class TestEmptyProjectFunctions(ProjectCreatingTestCase):
    """
    Test an empty project.
    """

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
        tests the creation and gradual deletion of a bunch of files

        note: no robot.py is created in this test
        """

        files = ["cows.py", "cheese", "monkeys.py"]
        self.asserted_create_files(files)
        for i in range(0, len(files)):
            self.asserted_delete_file(files[i])
            for remaining_file in files[i+1:]:
                self.assertFileExistsInProject(remaining_file)
