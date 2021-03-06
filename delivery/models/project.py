import os

from delivery.models import BaseModel


class Project(BaseModel):
    """
    Model a project directory in a runfolder on disk. Note that this means that this project model only extends
    to the idea of projects as subdirectories in a demultiplexed Illumina runfolder.
    """

    def __init__(self, name, path, runfolder_path=None):
        """
        Instantiate a new project object
        :param name: of the project
        :param path: path to the project
        :param runfolder_path: path the runfolder in which this project is stored.
        """
        self.name = name
        self.path = os.path.abspath(path)
        self.runfolder_path = runfolder_path

    def __eq__(self, other):
        """
        Two project should be considered the same if the represent the same directory on disk
        :param other: instance of Project
        :return: true if the same project, otherwise false
        """
        if isinstance(other, self.__class__):
            return self.path == other.path
        return False
