import os
from visualGPS.reader import FileReaderController
from visualGPS.parser import Parser


def main():
    dir = os.path.dirname(__file__)
    config = os.path.join(dir, 'config', 'config.yml')
    datafile = os.path.join(dir, 'data', '1950_5_01_L627_OMNI_0.GPS')
    filereader = FileReaderController(datafile, config)

    filereader.parse_frame_header(filereader.get_frame())
    print(filereader.header_structure)
    filereader.parse_frame_header(filereader.get_frame())
    print(filereader.header_structure)
    filereader.parse_frame_header(filereader.get_frame())
    print(filereader.header_structure)
    filereader.parse_frame_header(filereader.get_frame())
    print(filereader.header_structure)

if __name__ == "__main__":
    main()
