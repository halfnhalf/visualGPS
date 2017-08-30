import yaml
import sys
from abc import abstractmethod

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
        for field in self.content:
            self.header_structure[field[_CONFIG_NAME_KEY]] = self.get_field_data(field, frame_data)

    @staticmethod
    def get_field_data(field, frame_data):
        offset = field[_CONFIG_OFFSET_KEY]
        size = field[_CONFIG_SIZE_KEY]
        encode = field[_ENCODE_KEY] if _ENCODE_KEY in field else None

        if encode:
            return Reader._decode_field_data(frame_data[offset:offset+size], encode)
        else:
            return frame_data[offset:offset+size]


    @staticmethod
    def _decode_field_data(field_data, encode):
        decoded_data = {
            'int': lambda x: int.from_bytes(x, byteorder=sys.byteorder)
        }[encode](field_data)

        return decoded_data

    @abstractmethod
    def get_frame(self):
        raise NotImplementedError()


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
        self.binary_file = open(filename, "rb")

    def get_frame(self):
        """
        Get frames iteratively, one at a time
        """
        try:
            start_of_frame = self._seek_next_sync_bytes_pos(self.current_frame_pos)
            end_of_frame = self._seek_next_sync_bytes_pos(start_of_frame+self.num_sync_bytes)
            self.binary_file.seek(start_of_frame)
            self.current_frame_pos = end_of_frame
            frame = self.binary_file.read(end_of_frame-start_of_frame)

            self.digest_frame_header(frame)

            return frame

        except TypeError:
            print("No sync bytes found.")
            raise

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


import serial
class SerialReaderController(Reader):
    """
    this class is used to read data from a serial connection
    """

    def __init__(self, tty, configfile):
        """
        :param tty: the tty absolute path to read our serial connection from
        :param configfile: the configfile absolute path
        """

        super(SerialReaderController, self).__init__(configfile)
        self.tty = tty
        self.port_buffer = 100

        self.port = serial.Serial(tty)
        assert self.port.is_open

    def get_frame(self):
        found_first_sync = False
        found_second_sync = False
        buffer = self.port.read(self.port_buffer)
        (start_of_frame, found_first_sync) = self._seek_next_sync_bytes_pos(buffer, 0)

        while not found_first_sync:
            buffer = self.port.read(self.port_buffer)
            (start_of_frame, found_first_sync) = self._seek_next_sync_bytes_pos(buffer, 0)

        (end_of_frame, found_second_sync) = self._seek_next_sync_bytes_pos(buffer, start_of_frame+self.num_sync_bytes)
        while not found_second_sync:
            buffer = buffer + self.port.read(self.port_buffer)
            (end_of_frame, found_second_sync) = self._seek_next_sync_bytes_pos(buffer, 0)

        frame = buffer[start_of_frame:end_of_frame]
        self.digest_frame_header(frame)

        return buffer[start_of_frame:end_of_frame]

    def _seek_next_sync_bytes_pos(self, buffer, start_position):
        """
        :return : tuple (position, did we find sync?)
        """
        num_sync_bytes_found = 0

        for pos in range(len(buffer[start_position:])):
            byte = buffer[pos:pos+1]
            if byte == self.sync_bytes_list[num_sync_bytes_found]:
                num_sync_bytes_found += 1
                if num_sync_bytes_found == self.num_sync_bytes:
                    return (pos+start_position-self.num_sync_bytes, True)
            else:
                num_sync_bytes_found = 0
        return (0, False)
