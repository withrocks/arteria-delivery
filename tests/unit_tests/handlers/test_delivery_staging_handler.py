from mock import MagicMock

from tornado.testing import *
from tornado.web import Application

from delivery.app import routes

from tests.test_utils import DummyConfig, FAKE_RUNFOLDERS


class TestStagingHandlers(AsyncHTTPTestCase):

    API_BASE = "/api/1.0"

    mock_runfolder_repo = MagicMock()

    def get_app(self):
        return Application(
            routes(
                config=DummyConfig(),
                runfolder_repo=self.mock_runfolder_repo))

    ###
    # A staging handler should:
    # - be able start staging a folder at request, and return a id to be used for checking its status
    def test_start_staging_process(self):
        pass

    # - should not start staging a folder if there is already a ongoing staging effort for that folder
    def test_start_where_staging_in_progress(self):
        pass

    # - list stagings (paging the request is currently not in scope)
    def test_list_staging(self):
        pass

    # - list stagings with filters
    def test_list_staging_with_filter(self):
        pass

    # - change the status of staging attempts
    def test_change_staging_state(self):
        pass

    # - kill the process of a staging attempt
    def test_cancel_staging_process(self):
        pass
