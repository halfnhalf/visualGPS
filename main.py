from __future__ import division
import os
from visualGPS.reader import FileReaderController
from visualGPS.parser import ProPak6
from visualGPS import VisualGPS
from visualGPS.interface import start_tui

def main():
    dir = os.path.dirname(__file__)
    config = os.path.join(dir, 'config', 'config.yml')
    datafile = os.path.join(dir, 'data', '1950_5_01_L627_OMNI_0.GPS')

    gps = VisualGPS(config)
    gps.add_datafile(datafile)
    gps.register(ProPak6)
    gps.register(FileReaderController)

    #while True:
        #input("press a key to get next frame")
        #gps.get_frame()
        #print(gps.reader.header_structure)
        #print("hi")
    start_tui()

if __name__ == "__main__":
    main()
