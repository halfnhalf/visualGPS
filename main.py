import os
from visualGPS.reader import FileReaderController
from visualGPS.parser import Parser


def main():
    dir = os.path.dirname(__file__)
    config = os.path.join(dir, 'config', 'config.yml')
    datafile = os.path.join(dir, 'data', '1950_5_01_L627_OMNI_0.GPS')
    filereader = FileReaderController(datafile, config)
    parser = Parser(config)
    parser.parse_frame(filereader.get_frame())

if __name__ == "__main__":
    main()
