
import logging
import os
import re

from models.runfolder import Runfolder
from models.project import Project


log = logging.getLogger(__name__)


class DefaultFileSystemService(object):

    def _list_directories(self, base_path):

        log.debug("Listing dirs in: {}".format(os.path.abspath(base_path)))
        for my_dir in os.listdir(base_path):
            dir_abs_path = os.path.abspath(os.path.join(base_path, my_dir))

            if os.path.isdir(dir_abs_path):
                log.debug("Found dir: {}".format(dir_abs_path))
                yield dir_abs_path

    def find_project_directories(self, projects_base_dir):
        return self._list_directories(projects_base_dir)

    def find_runfolder_directories(self, base_path):
        return self._list_directories(base_path)


class FileSystemBasedRunfolderRepository(object):

    def __init__(self, base_path, file_system_service=DefaultFileSystemService()):
        self._base_path = base_path
        self.file_system_service = file_system_service

    def _get_runfolders(self):
        # TODO Filter based on expression for runfolders...
        runfolder_expression = r"^\d+_"

        directories = self.file_system_service.find_runfolder_directories(
            self._base_path)
        for directory in directories:
            if re.match(runfolder_expression, os.path.basename(directory)):

                name = os.path.basename(directory)
                path = os.path.join(self._base_path, directory)

                projects_base_dir = os.path.join(path, "Projects")
                project_directories = self.file_system_service.find_project_directories(
                    projects_base_dir)

                runfolder = Runfolder(name=name, path=path, projects=None)

                def project_from_dir(d):
                    return Project(name=os.path.basename(d), path=os.path.join(projects_base_dir, d), runfolder_path=path)

                # There are scenarios where there are no project directories in the runfolder,
                # i.e. when fastq files have not yet been divided into projects
                if project_directories:
                    runfolder.projects = map(
                        project_from_dir, project_directories)

                yield runfolder

    def get_runfolders(self):
        return self._get_runfolders()
