from confighelper import global_config_helper

# roboide imports
import roboide.model as model
from roboide.controllers.user import *

def get_team_dictionary():
    """
    Return a dict of teams that the user is in.
    """

    teams = {}
    groups = global_config_helper.get("DEFAULT.user.default_groups")
    my_teams = []
    for x in groups.split(" "):
        my_teams.append(int(x[4:]))

    for team in my_teams:
        try:
            teams[team] = model.TeamNames.get(team).name
        except:
            teams[team] = "Unnamed team"
    return teams
