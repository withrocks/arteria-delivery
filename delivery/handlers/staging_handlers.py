
import json
from tornado.web import HTTPError

from arteria.web.handlers import BaseRestHandler


from delivery.models.deliveries import DeliveryOrder


class StagingRunfolderHandler(BaseRestHandler):

    def initialize(self, staging_service, **kwargs):
        self.staging_service = staging_service

    def post(self, runfolder_id):
        """
        TODO
        :param runfolder_id:
        :return:
        """
        try:
            request_data = self.body_as_object()
        except ValueError:
            request_data = {}

        projects_to_stage = request_data.get("projects", [])

        staging_order_ids = self.staging_service.stage_runfolder(runfolder_id, projects_to_stage)
        status_end_points = map(lambda order_id: "{0}://{1}{2}".format(self.request.protocol,
                                                                       self.request.host,
                                                                       self.reverse_url("stage_status", order_id)),
                                staging_order_ids)

        self.write_json({'staging_order_links': status_end_points})


class StagingHandler(BaseRestHandler):

    def initialize(self, staging_service, **kwargs):
        self.staging_service = staging_service

    def get(self, stage_id):
        """
        Returns the current status of the of the staging order, or 404 if the order is unknown.
        Possible values for status are: pending, staging_in_progress, staging_successful, staging_failed
        """
        status = self.staging_service.get_status_of_stage_order(stage_id)
        if status:
            self.write_json({'status': status.name})
        else:
            self.set_status(404, reason='No stage order with id: {} found.'.format(stage_id))

    def delete(self, stage_id):
        pass
