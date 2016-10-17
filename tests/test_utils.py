
from models.project import Project
from models.runfolder import Runfolder

from mock import MagicMock

class TestUtils:
    DUMMY_CONFIG = {}


class DummyConfig:
    def __getitem__(self, key):
        return TestUtils.DUMMY_CONFIG[key]

fake_directories = ["160930_ST-E00216_0111_BH37CWALXX", "160930_ST-E00216_0112_BH37CWALXX"]
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
                                runfolder=_runfolder1),
                       Project(name="DEF_456",
                               path="/foo/160930_ST-E00216_0111_BH37CWALXX/Projects/DEF_456",
                               runfolder=_runfolder1)]

_runfolder2 = Runfolder(name="160930_ST-E00216_0112_BH37CWALXX",
                        path="/foo/160930_ST-E00216_0112_BH37CWALXX")

_runfolder2.projects = [Project(name="ABC_123",
                               path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/ABC_123",
                               runfolder=_runfolder2),
                       Project(name="DEF_456",
                               path="/foo/160930_ST-E00216_0112_BH37CWALXX/Projects/DEF_456",
                               runfolder=_runfolder2)]


FAKE_RUNFOLDERS = [_runfolder1, _runfolder2]


