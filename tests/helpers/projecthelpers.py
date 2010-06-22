
# Standard imports
import os

# roboide imports
from roboide.user import get_repopath

def get_repo_file_path(team):
    return get_repopath(team).replace('file:///', '/')

def get_project_path(team, project):
    return get_repo_file_path(team) + os.path.sep + project

def does_project_exist(team, project):
    project_path = get_project_path(team, project)
    return os.path.isdir(project_path)
