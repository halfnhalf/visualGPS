import yaml
from visualGPS.reader import Reader, _CONFIG_NAME_KEY
from abc import abstractmethod

_PAYLOAD_KEY = "payload"
_PAYLOAD_SIZE_KEY = "size_from_header_field"
_PAYLOAD_OFFSET_KEY = "offset"

_MESSAGES_KEY = "messages"
_MESSAGE_ID_KEY = "message_id"
_MESSAGE_FIELD_KEY = "fields"


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

    def parse_frame(self, frame, header_structure):
        self.current_frame = {}
        self.current_frame["payload_data"] = {}
        self.current_frame["payload_size"] = header_structure[self.payload_size_header_key]
        self.current_frame["message_enum"] = ""
        payload = frame[self.payload_offset:self.payload_offset+self.current_frame["payload_size"]]
        message_id = header_structure[_MESSAGE_ID_KEY]

        try:
            self.current_frame["message_enum"] = self.messages[message_id][_CONFIG_NAME_KEY]
            this_message_config = self.messages[message_id]

            for field_name_key, field in this_message_config[_MESSAGE_FIELD_KEY].items():
                self.current_frame["payload_data"][field_name_key] = Reader.get_field_data(field, payload)
        except KeyError:
            """
            the message id is not in our config or a there is a missing field.
            eventually this will have nice popup errors with more information
            """
            self.current_frame["message_enum"] = str(message_id)
            self.current_frame["payload_data"]["unknown_message"] = "unknown message"

        self.frame_count += 1
