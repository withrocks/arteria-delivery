import os

class Project(object):

    def __init__(self, name, path, runfolder = None):
        self.name = name
        self.path = path
        self.runfolder = runfolder

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return os.path.abspath(self.path) == os.path.abspath(other.path)
        return False
