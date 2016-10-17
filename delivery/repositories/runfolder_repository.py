
import os
import re

from models.runfolder import Runfolder
from models.project import Project

class DefaultFileSystemService(object):

    def find_project_directories(self, projects_base_dir):
        for dir in os.listdir(projects_base_dir):
            if os.path.isdir(dir):
                yield dir

    def find_runfolder_directories(self, base_path):
        for dir in os.listdir(base_path):
            if os.path.isdir(dir):
                yield dir


class FileSystemBasedRunfolderRepository(object):

    def __init__(self, base_path, file_system_service = DefaultFileSystemService()):
        self.base_path = base_path
        self.file_system_service = file_system_service


    def _get_runfolders(self):
        # TODO Filter based on expression for runfolders...
        runfolder_expression = r"^\d+_"

        directories = self.file_system_service.find_runfolder_directories()
        for directory in directories:
            if re.match(runfolder_expression, os.path.basename(directory)):

                name = directory
                path = os.path.join(self.base_path, directory)

                projects_base_dir = os.path.join(path, "Projects")
                project_directories = self.file_system_service.find_project_directories(projects_base_dir)

                runfolder = Runfolder(name=name, path=path, projects=None)

                def project_from_dir(d):
                    return Project(name=d, path=os.path.join(projects_base_dir, d), runfolder=runfolder)

                # There are scenarios where there are no project directories in the runfolder,
                # i.e. when fastq files have not yet been divided into projects
                if project_directories:
                    runfolder.projects = map(project_from_dir, project_directories)

                yield runfolder

    def get_runfolders(self):
        return self._get_runfolders()
