import yaml
import sys
from visualGPS import Reader
from abc import abstractmethod

_PAYLOAD_KEY = "payload"
_PAYLOAD_SIZE_KEY = "size_from_header_field"
_PAYLOAD_OFFSET_KEY = "offset"

_MESSAGES_KEY = "messages"
_MESSAGE_ID_KEY = "message_id"

class Parser():
    def __init__(self, configfile):
        self.configfile = yaml.load(open(configfile, 'r'))
        self.payload_structure = self.configfile[_PAYLOAD_KEY]
        self.payload_offset = self.payload_structure[_PAYLOAD_OFFSET_KEY]
        self.payload_size_header_key = self.payload_structure[_PAYLOAD_SIZE_KEY]
        self.messages = self.payload_structure[_MESSAGES_KEY]

        self.frame_count = 0

    @abstractmethod
    def parse_data(self, frame, header_structure):
        """
        this function needs to be implemented by a child class

        :param frame: includes the header structure
        """
        raise NotImplementedError()


class ProPak6(Parser):
    def __init__(self, configfile):
        super(ProPak6, self).__init__(configfile)
        self.message_enum = "None"

    def parse_data(self, frame, header_structure):
        self.payload_size = header_structure[self.payload_size_header_key]
        self.payload = frame[self.payload_offset:self.payload_offset+self.payload_size]
        self.payload_data = {}
        message_id = header_structure[_MESSAGE_ID_KEY]

        self.message_enum = self.messages[_MESSAGE_ID_KEY][message_id]["name"]
        if message_id == 43:
            self.payload_data["#ofobservers"] = 0
        elif message_id == 25:
            self.message_enum = "raw gps subframe"
        elif message_id == 973:
            self.message_enum = "raw sbas subframe"
        elif message_id == 1306:
            self.message_enum = "unkown"
        elif message_id == 41:
            self.message_enum = "raw ephemeris data"
        else:
            self.message_enum = "None"

        self.frame_count += 1
