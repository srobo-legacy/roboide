import unittest
from project_creating_test_case import ProjectCreatingTestCase
class TestHistory(ProjectCreatingTestCase):
    """
    tests various history related functions
    """

    def test_empty_project_history(self):
        self.connection.request("GET", "/gethistory/?team=%d&"

