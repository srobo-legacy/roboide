import ConfigParser

class ConfigHelper:
    """
    entirely static class for helping with configuration stuff
    """
    parser = ConfigParser.SafeConfigParser()

    def update_configuration(self, config_file_name):
        self.parser.read(config_file_name)

    def get(self, configuration_item_name):
        split = configuration_item_name.split(".")
        section = split[0]
        key = configuration_item_name[len(section)+1:]
        return self.parser.get(section, key)

global_config_helper = ConfigHelper()
