
import logging
import os
import re

from delivery.models.runfolder import Runfolder
from delivery.models.project import Project


log = logging.getLogger(__name__)


class DefaultFileSystemService(object):
    """
    File system service, used for accessing the file system in a way that can
    easily be mocked out in testing.
    """

    @staticmethod
    def _list_directories(base_path):
        """
        List all directories
        :param base_path: base path to list directories in.
        :return: a generator of paths to directories
        """

        log.debug("Listing dirs in: {}".format(os.path.abspath(base_path)))
        for my_dir in os.listdir(base_path):
            dir_abs_path = os.path.abspath(os.path.join(base_path, my_dir))

            if os.path.isdir(dir_abs_path):
                log.debug("Found dir: {}".format(dir_abs_path))
                yield dir_abs_path

    def find_project_directories(self, projects_base_dir):
        """
        Find project directories
        :param projects_base_dir: directory to list
        :return: a generator of paths to project directories
        """
        return self._list_directories(projects_base_dir)

    def find_runfolder_directories(self, base_path):
        """
        Find runfolder directories
        :param base_path: directory to list
        :return: a generator or paths to runfolder directories
        """
        return self._list_directories(base_path)


class FileSystemBasedRunfolderRepository(object):
    """
    Uses the file system as a source of truth for information about what runfolders are available.
    """

    def __init__(self, base_path, file_system_service=DefaultFileSystemService()):
        """
        Instantiate a new FileSystemBasedRunfolderRepository
        :param base_path: the directory where runfolders are stored
        :param file_system_service: a service which can access the file system.
        """
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
        """
        Get all runfolders
        :return: a generator of known runfolders
        """
        return self._get_runfolders()

    def get_runfolder(self, runfolder):
        """
        Get a Runfolder object matching the specified name
        :param runfolder: to look for
        :return: the matching runfolder, or None if no match
        :raises: a AssertionError if more than one runfolder was found
                matching the given name.
        """
        runfolders = self.get_runfolders()
        matching_name = [r for r in runfolders if r.name == runfolder]
        if len(matching_name) > 1:
            raise AssertionError("Found more than 1 runfolder matching: ".format(r))
        if len(matching_name) > 0 and matching_name[0]:
            return matching_name[0]
        else:
            return None
