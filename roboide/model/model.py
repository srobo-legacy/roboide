from elixir import *
import datetime
from roboide.model import metadata as __metadata__, DBSession as __session__

# Holds ID to team name mappings
class TeamNames(Entity):
    name = Field(String(40))

# Holds the setting name -> ID mapping
class Settings(Entity):
    # The setting name
    name = Field(String(40))
    # The setting description
    description = Field(String(140))

class RoboPresent(Entity):
    team = ManyToOne('TeamNames')
    present = Field(Boolean)

class RoboLogs(Entity):
    #The team
    team = ManyToOne('TeamNames')
    #Time log was written
    date = Field(DateTime, default=datetime.datetime.now)
    #Value written
    value = Field(UnicodeText)

# Holds the settings
class SettingValues(Entity):
    # The setting ID
    setting = ManyToOne('Settings')
    # The user that this setting is for
    uname = Field(String(40))
    # The setting value
    value = Field(String(40))

# Holds the autosaved files
class AutoSave(Entity):
    # The full file name and path
    file_path = Field(UnicodeText)
    # The revision that the file is based on
    revision = Field(Integer)
    # The team of the user that saved the file
    team = ManyToOne('TeamNames')
    # The user that saved the file
    uname = Field(String(40))
    # The date and time of the save, defaults to now
    date = Field(DateTime, default=datetime.datetime.now)
    # The file contents
    content = Field(UnicodeText)

class UserBlogFeeds(Entity):
	#the user id
	user = Field(String(40))
	#the url of the rss/atom feed
	url = Field(String(255))
	#validated by student robotics admin
	valid = Field(Boolean)
	#checked by student robotics admin
	checked = Field(Boolean)
