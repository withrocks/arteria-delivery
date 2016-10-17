import os
import unittest

from mock import patch, MagicMock

from models.runfolder import Runfolder
from models.project import Project
from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository


class TestRunfolderRepository(unittest.TestCase):

    fake_directories = ["160930_ST-E00216_0111_BH37CWALXX", "160930_ST-E00216_0112_BH37CWALXX"]
    fake_projects = ["ABC_123", "DEF_456"]

    @staticmethod
    def _mock_file_system_service(fake_directories, fake_projects):

        mock_file_system_service = MagicMock()
        mock_file_system_service.find_runfolder_directories.return_value = fake_directories
        mock_file_system_service.find_project_directories.return_value = fake_projects
        return mock_file_system_service

    runfolder1 = Runfolder(name="160930_ST-E00216_0111_BH37CWALXX",
                           path="/foo/160930_ST-E00216_0111_BH37CWALXX")

    runfolder1.projects = [Project(name="ABC_123",
                                   path="/foo/160930_ST-E00216_0111_BH37CWALXX/Projects/ABC_123",
                                   runfolder=runfolder1),
                           Project(name="DEF_456",
                                   path="/foo/160930_ST-E00216_0111_BH37CWALXX/Projects/DEF_456",
                                   runfolder=runfolder1)]

    runfolder2 = Runfolder(name="160930_ST-E00216_0112_BH37CWALXX",
                           path="/foo/160930_ST-E00216_0112_BH37CWALXX")

    runfolder2.projects = [Project(name="ABC_123",
                                   path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/ABC_123",
                                   runfolder=runfolder1),
                           Project(name="DEF_456",
                                   path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/DEF_456",
                                   runfolder=runfolder1)]

    expected_runfolders = [runfolder1, runfolder2]

    def test_get_runfolders(self):
        mock_file_system_service = TestRunfolderRepository._mock_file_system_service(self.fake_directories,
                                                                                     self.fake_projects)
        repo = FileSystemBasedRunfolderRepository(base_path="/foo",
                                                  file_system_service=mock_file_system_service)
        actual_runfolders = list(repo.get_runfolders())

        self.assertListEqual(self.expected_runfolders, actual_runfolders)

        for actual_runfolder in actual_runfolders:
            for expected_runfolder in self.expected_runfolders:
                if actual_runfolder == expected_runfolder:
                    self.assertListEqual(actual_runfolder.projects, expected_runfolder.projects)

    def test_get_runfolders_does_not_return_none_runfolder(self):
        # Adding a directory which does not conform to the runfolder pattern
        with_non_runfolder_dir = self.fake_directories + ["bar"]
        mock_file_system_service = TestRunfolderRepository._mock_file_system_service(with_non_runfolder_dir,
                                                                                     self.fake_projects)
        repo = FileSystemBasedRunfolderRepository(base_path="/foo",
                                                  file_system_service=mock_file_system_service)
        actual_runfolders = list(repo.get_runfolders())
        self.assertListEqual(self.expected_runfolders, actual_runfolders)

