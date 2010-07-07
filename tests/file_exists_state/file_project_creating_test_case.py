from tests.project_creating_test_case import ProjectCreatingTestCase
from roboide import vcs_bzr as bzr

class FileAndProjectCreatingTestCase(ProjectCreatingTestCase):
    def setUp(self):
        ProjectCreatingTestCase.setUp(self)
        self.projWrite = bzr.ProjectWrite(1, self.project_name)
        self.projWrite.update_file_contents("robot.py", "from sr import *\nprint 'ponies'\n")
        self.projWrite.commit("start")

    def tearDown(self):
        self.projWrite.destroy()
        ProjectCreatingTestCase.tearDown(self)
