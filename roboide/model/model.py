from turbogears.database import PackageHub
from elixir import *
import datetime
from custom_types.enum import Enum

hub = PackageHub("roboide")
__connection__ = hub

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
    setting_id = Field(Integer)
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
    team_id = Field(Integer)
    # The user that saved the file
    uname = Field(String(40))
    # The date and time of the save, defaults to now
    date = Field(DateTime, default=datetime.datetime.now)
    # The file contents
    content = Field(UnicodeText)

class FirmwareTargets(Entity):
    """Devices that we manage firmware for."""
    # The name of the device.
    name = Field(String(40))

class FirmwareBlobs(Entity):
    # The device (ForeignKey doesn't work in the sqlobject on button)
    device = Field(Integer) #ForeignKey("FirmwareTargets")

    # The version number
    version = Field(Integer)

    # The firmware filename
    firmware = Field(String(40))

    # The revision number in VC that the firmware is built from.
    # Current supported formats:
    #  - "svn:REV" where REV is the subversion commit number.
    #  - "git:SHA" where SHA is the git commit hash.
    revision = Field(String(40))

    # A description of the firmware.  Could contain a changelog.
    description = Field(UnicodeText)

class FirmwareState(Entity):
    # The firmware this relates to. (ForeignKey doesn't work in the sqlobject on button)
    fw_id = Field(Integer) #ForeignKey("FirmwareBlobs")

    # The date and time of state change
    date = Field(Date)

    # An message to go with the state change
    message = Field(UnicodeText)

    # The state the firmware changed to
    state = Field(Enum([
                                    "ALLOCATED",
                                    "DEVEL",
                                    "TESTING",
                                    "SHIPPING",
                                    "FAILED",
                                    "OLD_RELEASE",
                                    "SUPERCEDED"
                       ]
                , strict=True )
            )

class FirmwareTesting(Entity):
    # The firmware this relates to. (ForeignKey doesn't work in the sqlobject on button)
    fw_id = Field(Integer) #ForeignKey("FirmwareBlobs")

    # The date and time of the test result
    date = Field(Date)

    # An message to go with the test result
    message = Field(UnicodeText)

    # The result of the firmware test
    result = Field(Boolean)

class UserBlogFeeds(Entity):
	#the user id
	user = Field(String(40))
	#the url of the rss/atom feed
	url = Field(String(255))
	#validated by student robotics admin
	valid = Field(Boolean)
	#checked by student robotics admin
	checked = Field(Boolean)
