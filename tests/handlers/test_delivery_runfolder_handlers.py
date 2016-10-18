
import json
from mock import MagicMock


from tornado.testing import *
from tornado.web import Application

from delivery.app import routes

from tests.test_utils import DummyConfig, FAKE_RUNFOLDERS


class TestRunfolderHandlers(AsyncHTTPTestCase):

    API_BASE = "/api/1.0"

    mock_runfolder_repo = MagicMock()
    mock_runfolder_repo.get_runfolders.return_value = FAKE_RUNFOLDERS

    def get_app(self):
        return Application(
            routes(
                  config=DummyConfig(),
                  runfolder_repo=self.mock_runfolder_repo))

    def test_get_runfolders(self):
        response = self.fetch(self.API_BASE + "/runfolders")

        expected_result = {"runfolders": map(lambda x: x.to_json(), FAKE_RUNFOLDERS)}

        self.assertEqual(response.code, 200)
        self.assertDictEqual(json.loads(response.body), expected_result)

