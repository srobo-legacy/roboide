
# Standard imports
import os
import subprocess

# roboide imports
from roboide.user import get_repopath

def get_repo_file_path(team):
    """
    Return the path to a team's repo.
    """
    return get_repopath(team).replace('file:///', '/')

def get_project_path(team, project):
    """
    Return the full path to a project.
    """
    return get_repo_file_path(team) + os.path.sep + project

def does_project_exist(team, project):
    """
    Return whether or not a project exists in a team's repo.
    """
    project_path = get_project_path(team, project)
    return os.path.isdir(project_path)

def checkout_repository(team, project, todir):
    """
    Grab a temporary checkout of a team's repo.
    """
    subprocess.check_call(["bzr", "checkout", get_project_path(team, project), todir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def file_exists_in_project(file, team, project):
    """
    Return whether or not a file exists in a project.
    """
    checkout_path = "/tmp/repo"
    subprocess.call(["rm", "-rf", checkout_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    checkout_repository(team, project, checkout_path)

    result = os.path.isfile(checkout_path + os.path.sep + file)
    subprocess.call(["rm", "-rf", checkout_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result
