
import logging

from delivery.exceptions import InvalidStatusException
from delivery.models.db_models import StagingStatus, DeliveryStatus

log = logging.getLogger(__name__)


class MoverDeliveryService(object):

    def __init__(self, external_program_service, staging_service, delivery_repo):
        self.external_program_service = external_program_service
        self.staging_service = staging_service
        self.delivery_repo = delivery_repo

    def deliver_by_staging_id(self, staging_id, delivery_project):

        stage_order = self.staging_service.get_stage_order_by_id(staging_id)
        if not stage_order or stage_order.status == StagingStatus.staging_successful:
            raise InvalidStatusException("Only deliver by staging_id if it has a successful status!")

        # TODO Adjust staging_target to fit with exactly what we want to deliver
        delivery_order = self.delivery_repo.create_delivery_order(delivery_source=stage_order.staging_target,
                                                                  delivery_project=delivery_project,
                                                                  delivery_status=DeliveryStatus.pending,
                                                                  staging_order_id=staging_id)

        # TODO We need to figure out how to handle this once we know something about
        # how mover works...

    def get_status_of_delivery_order(self, delivery_order_id):
        pass

