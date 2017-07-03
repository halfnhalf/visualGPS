import yaml

_NUM_BYTES_TO_READ = 1


class Reader():
    def __init__(self, configfile):
        self.configfile = configfile
        self.sync_bytes_list = yaml.load(open(configfile, 'r'))['sync_bytes']
        self.sync_bytes_list = [bytes.fromhex(x) for x in self.sync_bytes_list]
        self.current_frame_pos = 0


class FileReaderController(Reader):
    """
    This class is used to read binary gps data from a file
    and deliver frames according to an API
    """

    def __init__(self, filename, configfile):
        super(FileReaderController, self).__init__(configfile)
        self.filename = filename
        self.num_sync_bytes = len(self.sync_bytes_list)

    def get_frame(self):
        """
        Get frames iteratively, one at a time
        """
        with open(self.filename, "rb") as self.binary_file:
            start_of_frame = self.seek_next_sync_bytes_pos(self.current_frame_pos)
            end_of_frame = self.seek_next_sync_bytes_pos(start_of_frame+self.num_sync_bytes)

        self.current_frame_pos = end_of_frame
        print(start_of_frame, end_of_frame)

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
