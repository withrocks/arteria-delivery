
import json

from delivery.models.deliveries import DeliveryOrder
from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler


class DeliverRunfolderHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        self.delivery_service = kwargs["delivery_service"]
        super(DeliverRunfolderHandler, self).initialize(kwargs)

    @staticmethod
    def _create_delivery_orders(runfolder, projects_to_deliver, delivery_project_id):

        # If no projects have been specified, delivery all projects
        if not projects_to_deliver:
            projects_to_deliver = runfolder.projects

        for project in runfolder.projects:
            if project in projects_to_deliver:
                yield DeliveryOrder(delivery_target=project.path, delivery_project_id=delivery_project_id)

    def post(self, runfolder_id):

        # TODO This is just a sketch that is not yet tested!

        request_data = self.body_as_object(["delivery_project_id"])
        delivery_project_id = request_data.get("delivery_project_id")
        projects_to_deliver = request_data.get("projects", [])

        runfolder = self.runfolder_repo.get_runfolder(runfolder_id)

        if runfolder and delivery_project_id:
            delivery_orders = self._create_delivery_orders(runfolder, projects_to_deliver)

            delivery_returns = []
            for order in delivery_orders:
                # TODO Figure out what to return here...
                delivery_returns.append(self.delivery_service.delivery(order))

            self.write_json(json.dumps({"delivery_status": delivery_returns}))
        else:
            self.write_error(404)

    def get(self, runfolder_id):
        # TODO Figure out if it's possible to get the status for a delivery like this...
        pass
