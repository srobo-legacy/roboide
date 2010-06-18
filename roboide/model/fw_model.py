from elixir import *
import datetime
from custom_types.enum import Enum
from roboide.model import metadata as __metadata__, DBSession as __session__

class FirmwareTargets(Entity):
    """Devices that we manage firmware for."""
    # The name of the device.
    name = Field(String(40))

class FirmwareBlobs(Entity):
    # The device
    device = ManyToOne("FirmwareTargets")

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
    # The firmware this relates to.
    firmware = ManyToOne("FirmwareBlobs")

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
    # The firmware this relates to.
    firmware = ManyToOne("FirmwareBlobs")

    # The date and time of the test result
    date = Field(Date)

    # An message to go with the test result
    message = Field(UnicodeText)

    # The result of the firmware test
    result = Field(Boolean)
