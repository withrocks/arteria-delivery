
import os
import json

class Runfolder(object):

    def __init__(self, name, path, projects = None):
        self.name = name
        self.path = path
        self.projects = projects

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return os.path.abspath(self.path) == os.path.abspath(other.path)
        return False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)