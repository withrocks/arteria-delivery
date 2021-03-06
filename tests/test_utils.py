
import time
from mock import MagicMock

from delivery.models.project import Project
from delivery.models.runfolder import Runfolder


class TestUtils:
    DUMMY_CONFIG = {"monitored_directory": "/foo"}


class DummyConfig:

    def __getitem__(self, key):
        return TestUtils.DUMMY_CONFIG[key]

fake_directories = ["160930_ST-E00216_0111_BH37CWALXX",
                    "160930_ST-E00216_0112_BH37CWALXX"]
fake_projects = ["ABC_123", "DEF_456"]


def mock_file_system_service(directories, projects):
    mock_file_system_service_instance = MagicMock()
    mock_file_system_service_instance.find_runfolder_directories.return_value = directories
    mock_file_system_service_instance.find_project_directories.return_value = projects
    return mock_file_system_service_instance

_runfolder1 = Runfolder(name="160930_ST-E00216_0111_BH37CWALXX",
                        path="/foo/160930_ST-E00216_0111_BH37CWALXX")

_runfolder1.projects = [Project(name="ABC_123",
                                path="/foo/160930_ST-E00216_0111_BH37CWALXX/Projects/ABC_123",
                                runfolder_path=_runfolder1.path),
                        Project(name="DEF_456",
                                path="/foo/160930_ST-E00216_0111_BH37CWALXX/Projects/DEF_456",
                                runfolder_path=_runfolder1.path)]

_runfolder2 = Runfolder(name="160930_ST-E00216_0112_BH37CWALXX",
                        path="/foo/160930_ST-E00216_0112_BH37CWALXX")

_runfolder2.projects = [Project(name="ABC_123",
                                path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/ABC_123",
                                runfolder_path=_runfolder2.path),
                        Project(name="DEF_456",
                                path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/DEF_456",
                                runfolder_path=_runfolder2.path)]


FAKE_RUNFOLDERS = [_runfolder1, _runfolder2]


def assert_eventually_equals(self, timeout, f, expected, delay=0.1):
    start_time = time.time()

    while True:
        try:
            value = f()
            self.assertEquals(value, expected)
            break
        except AssertionError:
            if time.time() - start_time <= timeout:
                time.sleep(delay)
                continue
            else:
                raise
