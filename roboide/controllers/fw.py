from turbogears import config, expose
from roboide import model
import cherrypy
import datetime, time
from hashlib import sha1 as sha
import os.path

# Import SR code
from roboide import sr

TEST_PASSES_TO_SHIP = 4

def datetime_to_stamp(d):
    return int( time.mktime( d.timetuple() ) )

class FwServe(object):
    @expose("json")
    def devices(self):
        """Get a list of devices"""
        s = model.FirmwareTargets.query.all()
        devices = [x.name for x in list(s)]
        return { "devices": devices }

    def __check_rev(self, rev):
        """Check that a string describing a revision is valid."""
        if rev == "dev":
            return True

        if len(rev) < len("svn:0"):
            return False

        if rev[0:4] not in ['svn:', 'git:']:
            return False

        # Check the SVN revision number is all numbers
        if rev[0:4] == 'svn:' and False in [x.isdigit() for x in rev[4:]]:
            return False

        # Check the GIT revision number is hex only
        if rev[0:4] == 'git:' and False in [x in '0123456798abcdef' for x in rev[4:]]:
            return False

        return True

    def __find_device(self, device):
        """Returns the ID of the given device"""
        r = model.FirmwareTargets.query.filter_by(name = device).all()

        if len(r) == 0:
            return False

        if len(r) > 1:
            raise "More than one device registered with the name '%s'" % device

        return r[0]

    def __find_new_ver(self, device):
        """Find a new, unused firmware version."""
        blobs = model.FirmwareBlobs.query.filter_by(device = device).all()

        if len(blobs) == 0:
            return 0

        return max([blob.version for blob in blobs]) + 1

    def __add_state(self, fw, message, state):
        """Add a status change message to a firmware image"""
        f = model.FirmwareState( firmware = fw,
                                 date = datetime.datetime.now(),
                                 message = message,
                                 state = state )

    def __get_state(self, fw):
        """Get the state of the given device image."""
        r = model.FirmwareState.query.filter_by(firmware = fw)
        r = r.order_by(model.FirmwareState.date).all()

        if len(r) == 0:
            return "NONE"

        latest = r[-1]

        return latest.state

    # In future will require login:
    @expose("json")
    def req_version(self,device,desc,revision):
        """Get a new version number for a firmware image."""

        if not self.__check_rev(revision):
            return {"ERROR": "Invalid VC revision string"}

        dev = self.__find_device(device)
        if dev == False:
            return {"ERROR": "Device '%s' not found" % device}

        version = self.__find_new_ver(dev)

        nver = model.FirmwareBlobs( device = dev,
                                    version = version,
                                    firmware = "JAM",
                                    revision = revision,
                                    description = desc )

        self.__add_state( fw = nver,
                          message = "Version number allocated",
                          state = "ALLOCATED" )

        return { "version" : version }

    # In future will require login:
    @expose("json")
    def upload(self,device,version,firmware):
        """Upload a firmware image to the system."""
        version = int(version)

        dev_id = self.__find_device(device)
        if dev_id == False:
            return {"ERROR": "Device '%s' not found" % device}

        # Check the version is correct
        r = model.FirmwareBlobs.query.filter_by(device = dev_id, version = version).all()

        if len(r) == 0:
            return {"ERROR": "Version %i does not exist" % version}
        fw = r[0]

        if self.__get_state(fw) != "ALLOCATED":
            return {"ERROR": "Firmware already uploaded"}

        data = firmware.file.read()

        s = sha.new()
        s.update( data )

        # Use the SHA1 as the filename
        fw.firmware = s.hexdigest()

        f = open( "%s/%s" % (config.get("firmware.dir"), fw.firmware), "w" )
        f.write( data )
        f.close()

        self.__add_state( fw, "Firmware uploaded", "DEVEL" )

        return { "sha1": s.hexdigest() }

    @expose()
    def get(self,device,version):
        """Return the firmware image for the given device."""
        version = int(version)
        dev_id = self.__find_device( device )

        if dev_id == False:
            return {"ERROR" : "Invalid device '%s'" % device}

        r = model.FirmwareBlobs.query.filter_by(version = version, device = dev_id).all()

        if len(r) == 0:
            return {"ERROR" : "Version '%i' doens't exist for device '%s'." % (version, device)}

        response.headers['Content-Type'] = "application/x-download"
        response.headers['Content-Disposition'] = 'attachment; filename="%s-%i"' % ( device, version )

        f = open( "%s/%s" % (config.get("firmware.dir"), r[0].firmware), "r" )

        return f.read()

    @expose("json")
    def info(self,device,version):
        """Return information about the given firmware image version."""
        version = int(version)

        dev_id = self.__find_device(device)
        if dev_id == False:
            return {"ERROR": "Device '%s' not found" % device}

        r = model.FirmwareBlobs.query.filter_by(device = dev_id, version = version).all()

        if len(r) == 0:
            return {"ERROR": "Version %i does not exist" % version}
        fw = r[0]

        r = model.FirmwareState.query.filter_by(firmware = fw)
        r = r.order_by(model.FirmwareState.date).all()
        log = []
        for entry in r:
            log.append( { "time": datetime_to_stamp(entry.date),
                          "message": entry.message,
                          "state": entry.state } )

        info = { "desc": fw.description,
                 "state": r[-1].state,
                 "log" : log }

        if info["state"] != "ALLOCATED":
            "The hash and size only make sense once the file's been uploaded "
            h = sha.new()
            f = open( "%s/%s" % (config.get("firmware.dir"), fw.firmware), "r" )
            h.update( f.read() )

            info["sha1"] = h.hexdigest();
            info["size"] = os.path.getsize( "%s/%s" % (config.get("firmware.dir"), fw.firmware));

        return info

    @expose("json")
    def images(self,device):
        """Return information about the firmwares for the given device."""
        dev = self.__find_device(device)
        if not dev:
            return {"ERROR": "Device '%s' not found" % device}

        state = {}
        for x in [ "ALLOCATED",
                   "DEVEL",
                   "TESTING",
                   "SHIPPING",
                   "FAILED",
                   "OLD_RELEASE",
                   "SUPERCEDED",
                   "NONE" ]:
            state[x] = []
        for fw in model.FirmwareBlobs.query.filter_by(device=dev).all():
            state[self.__get_state(fw)].append(fw.version)

        return state

    @expose("json")
    def sign(self,device,version,signature):
        """ """
        return "Firmware signing not yet implemented!"

    @expose("json")
    def submit(self,device,version):
        """Submit an image for testing"""
        version = int(version)
        dev_id = self.__find_device(device)
        if not dev_id:
            return {"ERROR": "Device '%s' not found" % device}

        r = model.FirmwareBlobs.query.filter_by(device=dev_id, version=version).all()
        if len(r) == 0:
            return {"ERROR": "Version '%i' does not exist" % version}
        fw = r[0]

        state = self.__get_state(fw)
        if state == 'ALLOCATED':
            return {"ERROR": "Cannot submit for testing without firmware image"}
        elif state == 'TESTING':
            return {"ERROR": "This firmware already under testing!"}
        elif state != 'DEVEL':
            return {"ERROR": "Cannot resubmit for testing"}

        for f in model.FirmwareBlobs.query.filter_by(device = dev_id).all():
            if self.__get_state(f) == 'TESTING':
                return {"ERROR": "Cannot submit more than one firmware for testing for device '%s'" % device}

        for f in model.FirmwareBlobs.query.filter_by(device = dev_id).all():
            if f.version < version and self.__get_state(f) in ['ALLOCATED','DEVEL']:
                self.__add_state(f, "Superceded by version %i" % version, "SUPERCEDED")

        self.__add_state(fw, "Submitted for Testing", "TESTING")

        return { "success": True }

    @expose("json")
    def submitresult(self,device,version,result,message=''):
        """Submit an image for testing"""
        version = int(version)
        dev_id = self.__find_device(device)
        if not dev_id:
            return {"ERROR": "Device '%s' not found" % device}

        r = model.FirmwareBlobs.query.filter_by(device = dev_id, version = version).all()
        if len(r) == 0:
            return {"ERROR": "Version '%i' does not exist" % version}
        fw = r[0]

        state = self.__get_state(fw)
        if state != 'TESTING':
            return {"ERROR": "Cannot submit result for firmware not currently under test"}

        if result not in ['pass','fail']:
            return {"ERROR": "Result must be one of 'pass' or 'fail'"}

        #convert to boolean
        result = (result == 'pass')
        #submit the result
        firmware_result = model.FirmwareTesting( firmware = fw,
                               date = datetime.datetime.now(),
                               message = message,
                               result = result )

        if not result:
            self.__add_state(fw, "Test Failure", "FAILED")
            tests_remaining = -1

        else:
            tests_passed = len(model.FirmwareTesting.query.filter_by(firmware = fw, result = True).all())
            tests_remaining = TEST_PASSES_TO_SHIP - tests_passed

            if tests_remaining == 0:
                for f in model.FirmwareBlobs.query.filter_by(device = dev_id).all():
                    if self.__get_state(f) == 'SHIPPING':
                        self.__add_state(f, "Replaced by version %i" % version, "OLD_RELEASE")
                        break

                self.__add_state(fw, "%i tests passed -- start shipping" % TEST_PASSES_TO_SHIP, "SHIPPING")

            else:
                self.__add_state(fw, "%i tests passed (%i needed)" % (tests_passed,TEST_PASSES_TO_SHIP), "TESTING")

        return { "success": True, "remaining": tests_remaining }
