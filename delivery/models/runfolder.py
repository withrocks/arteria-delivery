
import os

from delivery.models import BaseModel


class Runfolder(BaseModel):

    def __init__(self, name, path, projects=None):
        self.name = name
        self.path = path
        self.projects = projects

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return os.path.abspath(self.path) == os.path.abspath(other.path)
        return False
