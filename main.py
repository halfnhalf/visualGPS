import os
from visualGPS.reader.Reader import FileReaderController


def main():
    dir = os.path.dirname(__file__)
    config = os.path.join(dir, 'config', 'config.yml')
    filereader = FileReaderController("junk", config)

if __name__ == "__main__":
    main()
