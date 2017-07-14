import yaml
import sys
from abc import abstractmethod
from visualGPS.reader import _CONFIG_HEADER_KEY

_PAYLOAD_KEY = "payload"
_PAYLOAD_SIZE_KEY = "size_from_header_field"
_PAYLOAD_OFFSET_KEY = "offset"

class Parser():
    def __init__(self, configfile):
        self.configfile = yaml.load(open(configfile, 'r'))
        self.payload_structure = self.configfile[_PAYLOAD_KEY]
        self.payload_offset = self.payload_structure[_PAYLOAD_OFFSET_KEY]
        self.payload_size_header_key = self.payload_structure[_PAYLOAD_SIZE_KEY]

    @abstractmethod
    def parse_data(self, frame, header_structure):
        """
        this function needs to be implemented by a child class
        """
        raise NotImplementedError()

class ProPak6(Parser):
    def __init__(self, configfile):
        super(ProPak6, self).__init__(configfile)

    def parse_data(self, frame, header_structure):
        self.payload_size = header_structure[self.payload_size_header_key]
        self.payload = frame[self.payload_offset:self.payload_offset+self.payload_size]

        if(header_structure["response_id"] == 38):
            print("unknown status")
