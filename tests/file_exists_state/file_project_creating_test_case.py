from tests.project_creating_test_case import ProjectCreatingTestCase
from roboide import vcs_bzr as bzr

class FileAndProjectCreatingTestCase(ProjectCreatingTestCase):
    """
    Creates a project and a robot.py for testing the syntax checker.
    """

    def setUp(self):
        ProjectCreatingTestCase.setUp(self)
        self.projWrite = bzr.ProjectWrite(self.team, self.project_name, revno=self.rev)
        self.projWrite.update_file_contents("robot.py", "from sr import *\nprint 'ponies'\n")
        self.projWrite.commit("start")
        self.rev += 1
        self.projWrite.destroy()
        self.projWrite = None

    def tearDown(self):
        if self.projWrite is not None:
            self.projWrite.destroy()
            self.projWrite = None
        ProjectCreatingTestCase.tearDown(self)
