
# Standard imports
import os

# roboide imports
from roboide.user import get_repopath

def does_project_exist(team, project):
    repo_path = get_repopath(team).replace('file:///','/')
    project_path = repo_path + os.path.sep + project
    print project_path
    return os.path.isdir(project_path)
