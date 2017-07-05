import yaml

class Parser():
    def __init__(self, configfile):
        self.configfile = configfile
        self.content = yaml.load(open(configfile, 'r'))['content']
        print(self.content)
