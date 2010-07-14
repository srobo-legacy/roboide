import ConfigParser
import sys

class ConfigHelper:
    """
    entirely static class for helping with configuration stuff
    """
    parser = ConfigParser.SafeConfigParser()

    def update_configuration(self, config_file_name):
        print "parsertag", self.parser.read(config_file_name)
        sys.stdout.flush()

    def get(self, configuration_item_name):
        section,key = configuration_item_name.split(".")
        print section, key
        print "sectionsflag", self.parser.sections()
        sys.stdout.flush()
        return self.parser.get(section, key)

global_config_helper = ConfigHelper()
