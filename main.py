import os
from visualGPS.reader import FileReaderController
from visualGPS.parser import ProPak6


def main():
    dir = os.path.dirname(__file__)
    config = os.path.join(dir, 'config', 'config.yml')
    datafile = os.path.join(dir, 'data', '1950_5_01_L627_OMNI_0.GPS')
    filereader = FileReaderController(datafile, config)

    while True:
        input("press a key to get next frame")
        frame = filereader.get_frame()
        filereader.digest_frame_header(frame)
        parser = ProPak6(config, filereader.header_structure)
        parser.parse_data(frame)

if __name__ == "__main__":
    main()
