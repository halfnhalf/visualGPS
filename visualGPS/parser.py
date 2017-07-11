import yaml

_PAYLOAD_KEY = "payload"
_PAYLOAD_SIZE_KEY = "size_from_header_field"
_PAYLOAD_OFFSET_KEY = "offset"

class Parser():
    def __init__(self, configfile, header_structure):
        self.configfile = yaml.load(open(configfile, 'r'))
        self.payload_structure = self.configfile[_PAYLOAD_KEY]
        self.payload_offset = self.payload_structure[_PAYLOAD_OFFSET_KEY]
        self.header_structure = header_structure

        payload_size_header_key = self.payload_structure[_PAYLOAD_SIZE_KEY]
        self.payload_size = self.header_structure[payload_size_header_key]

        print(self.payload_size)


class ProPak6(Parser):
    def __init__(self, configfile, header_structure):
        super(ProPak6, self).__init__(configfile, header_structure)

    def parse_data(self, frame):
        print(frame[self.payload_offset:self.payload_offset+self.payload_size])
