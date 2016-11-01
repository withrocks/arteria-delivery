

import json
import os
from mock import MagicMock


from tornado.testing import *
from tornado.web import Application

from arteria.web.app import AppService

from delivery.app import routes as app_routes
from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository


class TestIntegration(AsyncHTTPTestCase):

    API_BASE = "/api/1.0"

    def get_app(self):

        # Get an as similar app as possible, tough note that we don't use the
        #  app service start method to start up the the application
        path_to_this_file = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__)))
        app_svc = AppService.create(product_name="test_delivery_service",
                                    config_root="{}/../../config/".format(path_to_this_file))

        config = app_svc.config_svc
        runfolder_repo = FileSystemBasedRunfolderRepository(
            config["monitored_directory"])

        return Application(app_routes(config=config, runfolder_repo=runfolder_repo))

    def test_can_return_flowcells(self):
        response = self.fetch(self.API_BASE + "/runfolders")

        self.assertEqual(response.code, 200)

        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)

        first_runfolder = response_json["runfolders"][0]
        self.assertEqual(first_runfolder["name"], "160930_ST-E00216_0111_BH37CWALXX")

    def test_can_return_projects(self):
        response = self.fetch(self.API_BASE + "/projects")
        self.assertEqual(response.code, 200)

        response_json = json.loads(response.body)
        self.assertEqual(len(response_json), 1)

        first_project = response_json["projects"][0]
        self.assertEqual(first_project["name"], "ABC_123")

    def test_can_stage_delivery(self):
        pass

    def test_can_deliver_data(self):
        pass
