import yaml
import sys

_NUM_BYTES_TO_READ = 1
_CONFIG_HEADER_KEY = 'header_structure'
_CONFIG_OFFSET_KEY = 'offset'
_CONFIG_SIZE_KEY = 'size'
_CONFIG_NAME_KEY = 'name'
_SYNC_BYTES_KEY = 'sync_bytes'
_ENCODE_KEY = 'encode'


class Reader():
    """
    This class gives the basic ability to read config and parse header information from a frame.
    This class requires a child class to actually obtain the frame data
    """
    def __init__(self, configfile):
        """
        Reader needs a configfile

        :param configfile: the config file absolute path
        """
        self.configfile = yaml.load(open(configfile, 'r'))
        self.sync_bytes_list = self.configfile[_SYNC_BYTES_KEY]
        self.content = self.configfile[_CONFIG_HEADER_KEY]
        self.sync_bytes_list = [bytes.fromhex(x) for x in self.sync_bytes_list]
        self.num_sync_bytes = len(self.sync_bytes_list)
        self.header_structure = {}
        self.current_frame_pos = 0

    def digest_frame_header(self, frame_data):
        self.frame_data = frame_data

        for field in self.content:
            self.header_structure[field[_CONFIG_NAME_KEY]] = self._get_field_data(field)

    def _get_field_data(self, field):
        offset = field[_CONFIG_OFFSET_KEY]
        size = field[_CONFIG_SIZE_KEY]
        encode = field[_ENCODE_KEY] if _ENCODE_KEY in field else None

        if encode:
            return self._decode_field_data(self.frame_data[offset:offset+size], encode)
        else:
            return self.frame_data[offset:offset+size]


    def _decode_field_data(self, field_data, encode):
        decoded_data = {
            'int': lambda x: int.from_bytes(x, byteorder=sys.byteorder)
        }[encode](field_data)

        return decoded_data

class FileReaderController(Reader):
    """
    This class is used to read binary gps data from a file
    and deliver frames
    """

    def __init__(self, filename, configfile):
        """
        FileReaderController

        :param filename: filename absolute path that you want to digest
        :param configfile: the configfile absolute path
        """
        super(FileReaderController, self).__init__(configfile)
        self.filename = filename

    def get_frame(self):
        """
        Get frames iteratively, one at a time
        """
        with open(self.filename, "rb") as self.binary_file:
            start_of_frame = self._seek_next_sync_bytes_pos(self.current_frame_pos)
            end_of_frame = self._seek_next_sync_bytes_pos(start_of_frame+self.num_sync_bytes)
            self.binary_file.seek(start_of_frame)
            self.current_frame_pos = end_of_frame
            return self.binary_file.read(end_of_frame-start_of_frame)

    def _seek_next_sync_bytes_pos(self, start_position):
        """
        this function requires a file stream to already be opened as
        self.binary_file

        seek and return the start of the next consecutive sync bytes
        """

        self.binary_file.seek(start_position)
        bytes_read = self.binary_file.read(1)
        num_sync_bytes_found = 0

        while bytes_read != b'':
            if bytes_read == self.sync_bytes_list[num_sync_bytes_found]:
                num_sync_bytes_found += 1
                if num_sync_bytes_found == self.num_sync_bytes:
                    return self.binary_file.tell()-self.num_sync_bytes
            else:
                num_sync_bytes_found = 0
            bytes_read = self.binary_file.read(1)
