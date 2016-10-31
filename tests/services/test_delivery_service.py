import unittest
from mock import MagicMock

from delivery.services.delivery_service import MoverDeliveryService
from delivery.models.deliveries import DeliveryOrder
from delivery.models.runfolder import Runfolder


class TestMoverDeliveryService(unittest.TestCase):

    mock_external_program_service = MagicMock()
    mover_delivery_service = MoverDeliveryService(mock_external_program_service)

    def test_deliver(self):
        # TODO Improve test once we have some logic here...
        delivery_target = MagicMock()
        delivery_order = DeliveryOrder(delivery_target=delivery_target,
                                       delivery_project="a2009002")
        self.mover_delivery_service.deliver(delivery_order)

    def test__status_for_delivery_id(self):
        # TODO Improve test once we have some logic here...
        pass

    def test__status_for_delivery_target(self):
        # TODO Improve test once we have some logic here...
        pass
