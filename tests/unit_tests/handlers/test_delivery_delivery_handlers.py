
import json
from mock import MagicMock


from tornado.testing import *
from tornado.web import Application

from delivery.app import routes

from tests.test_utils import DummyConfig, FAKE_RUNFOLDERS


class TestDeliveryHandlers(AsyncHTTPTestCase):

    API_BASE = "/api/1.0"

    mock_runfolder_repo = MagicMock()

    def get_app(self):
        self.mock_runfolder_repo.get_runfolders.return_value = FAKE_RUNFOLDERS
        self.mock_runfolder_repo.get_runfolder.return_value = FAKE_RUNFOLDERS[0]

        return Application(
            routes(
                config=DummyConfig(),
                runfolder_repo=self.mock_runfolder_repo))

    def test_post_delivery_runfolder(self):
        # TODO Write tests
        pass
