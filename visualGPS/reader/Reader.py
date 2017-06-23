import yaml


class Reader():
    def __init__(self, configfile):
        self.configfile = configfile
        self.sync_bytes = yaml.load(open(configfile, 'r'))['sync_bytes']
        print(self.sync_bytes)


class FileReaderController(Reader):
    """
    This class is used to read binary gps data from a file
    and parse it according to a config file
    """

    def __init__(self, filename, configfile):
        super(FileReaderController, self).__init__(configfile)
        self.filename = filename

    def get_frame():
        pass
