
from tornado.web import HTTPError

from arteria.web.handlers import BaseRestHandler


from delivery.models.deliveries import DeliveryOrder




class StagingRunfolderHandler(BaseRestHandler):

    def initialize(self, staging_service, runfolder_repo, deliveries_repository, **kwargs):
        self.staging_service = staging_service
        self.runfolder_repo = runfolder_repo
        self.deliveries_repo = deliveries_repository


    def post(self, runfolder_id):
        """
        TODO
        :param runfolder_id:
        :return:
        """
        request_data = self.body_as_object(["delivery_project_id"])
        delivery_project_id = request_data.get("delivery_project_id")
        projects_to_deliver = request_data.get("projects", [])

        runfolder = self.runfolder_repo.get_runfolder(runfolder_id)

        if not runfolder:
            raise HTTPError(404, reason="Couldn't find runfolder matching: {}".format(runfolder_id))

        # If no projects have been specified, stage all projects
        if not projects_to_deliver:
            projects_to_deliver = runfolder.projects

        for project in runfolder.projects:
            if project in projects_to_deliver:
                existing_delivery_orders = self.deliveries_repo.get_delivery_orders_for_source(project.path)


        # TODO Check repository for delivery orders matching the given runfolder

        # TODO This creation should probably happen via repository instead!
        #delivery_orders = create_delivery_orders_from_runfolder(runfolder, projects_to_deliver, delivery_project_id)

        for delivery_order in delivery_orders:
            self.staging_service.stage_order(delivery_order)


        # TODO!
        self.write_object({'yes': 'no'})

    # TODO Change this!
    def get(self, runfolder_id):
        """
        TODO
        :param runfolder_id:
        :return:
        """
        pass
