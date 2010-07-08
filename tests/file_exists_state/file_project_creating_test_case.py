from tests.project_creating_test_case import ProjectCreatingTestCase
from roboide import vcs_bzr as bzr

class FileAndProjectCreatingTestCase(ProjectCreatingTestCase):
    """
    Creates a project and a robot.py for testing the syntax checker.
    """

    def setUp(self):
        ProjectCreatingTestCase.setUp(self)
        projWrite = bzr.ProjectWrite(self.team, self.project_name, revno=self.rev)
        projWrite.update_file_contents("robot.py", "from sr import *\nprint 'ponies'\n")
        projWrite.commit("start")
        self.rev += 1
        projWrite.destroy()

    def tearDown(self):
        ProjectCreatingTestCase.tearDown(self)
