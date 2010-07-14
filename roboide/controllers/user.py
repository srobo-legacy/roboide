
# Turbogears imports
from tg import config, expose
from roboide import model
import cherrypy
from paste.deploy.converters import asbool, aslist

# Import SR code
from roboide import sr

def anon_login():
    """LDAP Anonymous Login"""
    password = config.get("ldap.anonpass")
    return (config.get("ldap.anonuser"),password)

# Bind to LDAP with the anonymous user to access user information
sr.set_userinfo( anon_login )

def require(*conditions):
    """Returns a decorator that enforces the given conditions.
    conditions is a list of is a function that returns True or False.
    cherrypy.HTTPError(401) is raised if a condition evaluates to be False."""
    def d(fn):
        def decorated( *args, **keywords ):
            if False in [condition() for condition in conditions]:
                raise cherrypy.HTTPError( 401, "Authorisation required" )
            return fn(*args, **keywords)
        return decorated
    return d

def in_team():
    """Returns a function that returns True if the current user is in a team"""
    return lambda: len(getteams()) > 0

def is_ide_admin():
    """Returns True if the current user is an IDE Admin, False otherwise"""
    if dev_env() and not use_ldap():
        return asbool(config.get( "user.can_admin" ))
    else:
        username = get_curuser()
        if username == None or username not in sr.users.list():
            return False
        else:
            return "ide-admin" in sr.user(username).groups()

class User(object):
    @expose("json")
    def info(self):
        """Returns a variety of information about the user
        outputs:
          - teams: dict mapping team numbers to team names."""
        user = get_curuser()
        if user == None:
            return {}

        teams = {}
        for team in getteams():
            rows = model.TeamNames.get_by(id=team)
            if rows is None:
                teams[team] = "Unnamed team"
            else:
                teams[team] = rows.first().name


        # Get the setting values
        svals = model.SettingValues.query.filter_by(uname = user)
        settings = {}
        for sval in svals.all():
            settings[sval.setting.name] = sval.value

        return { "user" : user,
                 "teams" : teams,
                 "settings": settings,
                 "can_admin": is_ide_admin() }

    @expose("json")
    def login(self, usr="",pwd=""):
        """Logs the given user in with the given password.
        Returns SUCCESS if authentication was successful, and FAIL if
        it was unsuccessful.
        If no username and password are given, then SUCCESS is
        returned if we're already logged in -- otherwise FAIL.

        Where: SUCCESS is {"login":1}
        and FAIL is {"login":0}"""

        SUCCESS = {"login" : 1}
        FAIL = {"login": 0}

        # When not using LDAP, logins are always successful
        if dev_env() and not use_ldap():
            return SUCCESS

        if usr == "" and pwd == "":
            # Already logged in
            if get_curuser() != None:
                return SUCCESS

        if pwd == "":
            return FAIL

        u = sr.user( usr )
        if not u.in_db:
            return FAIL

        if u.bind( pwd ):
            cherrypy.session["user"] = usr
            return SUCCESS
        else:
            return FAIL

    @expose("json")
    def logout(self):
        cherrypy.session.clear()
        return {}

    def set_setting(self, name, value, description=""):
        """set one of the user settngs as specified by name."""
        sids = model.Settings.query.filter_by(name = name)
        if sids.count() > 0:
            s = sids.first()
        else:
            s = self.add_setting(name, description)
        user = str(get_curuser())
        settings = model.SettingValues.query.filter_by(
                uname = user,
                setting = s
            )
        if(settings.count() > 0):  #if it exists update it
            settings.first().value = value
        else:
            model.SettingValues(uname = user, setting = s, value = value)
        return

    def add_setting(self, name, description):
        """add a possible user settng as specified by name."""
        return model.Settings(name = name, description = description)

def dev_env():
    """Returns True if we're in a development environment"""
    return asbool(config.get( "debug" ))

def use_ldap():
    """Returns True if we're using ldap"""
    return asbool(config.get( "user.use_ldap" ))

def get_curuser():
    """Returns the user we're currently acting as.
    Returns None if not logged in."""

    if dev_env() and not use_ldap():
        return config.get( "user.default" )
    else:
        # Use LDAP
        if not cherrypy.session.has_key( "user" ):
            return None
        return cherrypy.session["user"]

def getteams():
    """Return a list of the teams the user's in"""
    username = get_curuser()
    if username == None:
        return []

    groups = None

    if dev_env() and not use_ldap():
        # Use the default group list when not using LDAP
        groups = aslist(config.get( "user.default_groups" ))
    else:
        if username in sr.users.list():
            user = sr.user(username)
            groups = user.groups()
        else:
            return RuntimeError("Could not find user")

    return [int(group[4:]) for group in groups if group[:4] == "team"]

def get_repopath( team ):
    """Return the subversion repository URL for the current user and given team.
    Given team must be an integer."""
    return config.get( "repo.path" ).replace( "TEAM", str(team) )
