class ParseController:
    def __init__(fileorserial):
        self.fileorserial = fileorserial
        
        if fileorserial.startswith('/dev/tty'):
            self.usecom = False

    def parse_frame()
