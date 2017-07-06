import yaml

CONFIG_HEADER_KEY = 'header_structure'
CONFIG_OFFSET_KEY = 'offset'
CONFIG_SIZE_KEY = 'size'
CONFIG_NAME_KEY = 'name'

class Parser():
    def __init__(self, configfile):
        self.configfile = configfile
        self.content = yaml.load(open(configfile, 'r'))[CONFIG_HEADER_KEY]
        self.header_structure = {}

    def parse_frame(self, frame_data):
        self.frame_data = frame_data

        for field in self.content:
            self.header_structure[field[CONFIG_NAME_KEY]] = self._get_field_data(field)

    def _get_field_data(self, field):
        offset = field[CONFIG_OFFSET_KEY]
        size = field[CONFIG_SIZE_KEY]

        return self.frame_data[offset:offset+size]
