
import logging

from delivery.models.db_models import DeliveryOrder, DeliveryIdentifier
from delivery.services.external_program_service import ExternalProgramService

log = logging.getLogger(__name__)


class BaseDeliveryService(object):

    def deliver(self, delivery_order):
        if isinstance(delivery_order, DeliveryOrder):
            return self._deliver(delivery_order)
        else:
            raise NotImplementedError("Only DeliveryOrder is valid input to the deliver method")

    def _deliver(self, delivery_order):
        raise NotImplementedError("Must be implemented by subclass")

    def status(self, delivery_target_or_delivery_id):
        if isinstance(delivery_target_or_delivery_id, DeliveryOrder):
            log.debug("Got a delivery order, will try to find the status for it...")
            return self._status(delivery_target_or_delivery_id)
        elif isinstance(delivery_target_or_delivery_id, DeliveryIdentifier):
            log.debug("Got a delivery identifier, will try to find status for it...")
            return self._status_for_delivery_id(delivery_target_or_delivery_id)
        else:
            raise NotImplementedError("{} is not a valid type for checking the the status of a delivery".format(
                type(delivery_target_or_delivery_id)))

    def _status_for_delivery_target(self):
        raise NotImplementedError("Must be implemented by subclass")

    def _status_for_delivery_id(self):
        raise NotImplementedError("Must be implemented by subclass")


class MoverDeliveryService(BaseDeliveryService):

    def __init__(self, external_program_service):
        self.external_program_service = ExternalProgramService()

    def _deliver(self, delivery_order):
        pass

    def _status_for_delivery_id(self, delivery_id):
        log.debug("Will query Mover about status for delivery id: {}".format(delivery_id.id))
        # TODO
        pass

    def _status_for_delivery_target(self, delivery_target):
        log.debug("Will query Mover about delivery status of directory: {}".format(
            delivery_target.delivery_target))
        # TODO
        pass
