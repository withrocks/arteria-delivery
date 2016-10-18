import os
import unittest

from mock import patch, MagicMock

from models.runfolder import Runfolder
from models.project import Project
from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository

from tests.test_utils import FAKE_RUNFOLDERS, mock_file_system_service, fake_directories, fake_projects


class TestRunfolderRepository(unittest.TestCase):

    expected_runfolders = FAKE_RUNFOLDERS

    file_system_service = mock_file_system_service(fake_directories,
                                                   fake_projects)
    repo = FileSystemBasedRunfolderRepository(base_path="/foo",
                                              file_system_service=file_system_service)

    def test_get_runfolders(self):
        actual_runfolders = list(self.repo.get_runfolders())

        self.assertListEqual(self.expected_runfolders, actual_runfolders)

        for actual_runfolder in actual_runfolders:
            for expected_runfolder in self.expected_runfolders:
                if actual_runfolder == expected_runfolder:
                    self.assertListEqual(
                        actual_runfolder.projects, expected_runfolder.projects)

    def test_get_runfolders_does_not_return_none_runfolder(self):
        # Adding a directory which does not conform to the runfolder pattern
        with_non_runfolder_dir = fake_directories + ["bar"]
        file_system_service = mock_file_system_service(with_non_runfolder_dir,
                                                       fake_projects)
        repo = FileSystemBasedRunfolderRepository(base_path="/foo",
                                                  file_system_service=file_system_service)
        actual_runfolders = list(repo.get_runfolders())
        self.assertListEqual(self.expected_runfolders, actual_runfolders)

    def test_get_runfolder(self):
        runfolder_name = "160930_ST-E00216_0111_BH37CWALXX"
        actual_runfolder = self.repo.get_runfolder(runfolder_name)
        self.assertIsInstance(actual_runfolder, Runfolder)
        self.assertEqual(actual_runfolder.name, runfolder_name)
