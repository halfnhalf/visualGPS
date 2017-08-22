from visualGPS.reader import Reader
from visualGPS.parser import Parser

class VisualGPS():
    def __init__(self, configfile):
        self.configfile = configfile
        self.reader = None
        self.parser = None
        self.datafile = None
    
    def add_data_or_port(self, datafile):
        self.datafile = datafile

    def register(self, ClassName):
        if issubclass(ClassName, Reader):
            self.ReaderClass = ClassName
            self.reader = self.ReaderClass(self.datafile, self.configfile)

        if issubclass(ClassName, Parser):
            self.ParserClass = ClassName
            self.parser = self.ParserClass(self.configfile)

    def get_frame(self):
        frame = self.reader.get_frame()
        self.parser.parse_frame(frame, self.reader.header_structure)
