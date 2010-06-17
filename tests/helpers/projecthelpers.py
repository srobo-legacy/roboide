#munge path to include roboide
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0 : slice_end+1]+"../../")

# Standard imports
import os

# roboide imports
import roboide.model as model

def does_project_exist(team, project):
    team_number = str(team)
    team_path = team_number + "/" + project
    return os.path.isdir("../repos/" + team_path)
