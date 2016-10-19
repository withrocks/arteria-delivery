
import json
from mock import MagicMock


from tornado.testing import *
from tornado.web import Application

from delivery.app import routes

from tests.test_utils import DummyConfig, FAKE_RUNFOLDERS


class TestProjectHandlers(AsyncHTTPTestCase):

    API_BASE = "/api/1.0"

    mock_runfolder_repo = MagicMock()

    def get_app(self):
        self.mock_runfolder_repo.get_runfolders.return_value = FAKE_RUNFOLDERS
        self.mock_runfolder_repo.get_runfolder.return_value = FAKE_RUNFOLDERS[0]

        return Application(
            routes(
                config=DummyConfig(),
                runfolder_repo=self.mock_runfolder_repo))

    def test_get_projects(self):
        response = self.fetch(self.API_BASE + "/projects")

        expected_result = []
        for runfolder in FAKE_RUNFOLDERS:
            for project in runfolder.projects:
                expected_result.append(project.__dict__)

        self.assertEqual(response.code, 200)
        self.assertDictEqual(json.loads(response.body), {"projects": expected_result})

    def test_get_projects_empty(self):
        self.mock_runfolder_repo.get_runfolders.return_value = []

        response = self.fetch(self.API_BASE + "/projects")

        self.assertEqual(response.code, 200)
        self.assertDictEqual(json.loads(response.body), {"projects": []})

    def test_get_projects_for_runfolder(self):
        response = self.fetch(
            self.API_BASE + "/runfolder/160930_ST-E00216_0111_BH37CWALXX/projects")
        self.assertEqual(response.code, 200)
        self.assertTrue(len(json.loads(response.body)["projects"]) == 2)
