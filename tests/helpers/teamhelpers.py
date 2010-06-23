#munge path to include roboide
import sys
slice_end = __file__.rfind("/");
sys.path.append(__file__[0:slice_end+1]+"../../")

# TurboGears imports
from turbogears import config

# roboide imports
import roboide.model as model
from roboide.user import *

def get_team_dictionary():
    """
    Return a dict of teams that the user is in.
    """
    teams = {}
    groups = config.get("user.default_groups")
    my_teams = [int(group[4:]) for group in groups if group[:4] == "team"]

    for team in getteams():
        try:
            teams[team] = model.TeamNames.get(team).name
        except:
            teams[team] = "Unnamed team"

    return teams
