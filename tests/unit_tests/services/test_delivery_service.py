import unittest
from mock import MagicMock

from delivery.services.delivery_service import MoverDeliveryService
from delivery.models.db_models import DeliveryOrder
from delivery.models.runfolder import Runfolder
from delivery.exceptions import InvalidStatusException


class TestMoverDeliveryService(unittest.TestCase):

    def setUp(self):

        self.mock_external_program_service = MagicMock()
        self.mock_staging_service = MagicMock()
        self.mock_delivery_repo = MagicMock()
        self.mover_delivery_service = MoverDeliveryService(external_program_service=self.mock_external_program_service,
                                                           staging_service=self.mock_staging_service,
                                                           delivery_repo=self.mock_delivery_repo)

    def test_deliver_by_staging_id(self):
        # TODO
        pass

    def test_deliver_by_staging_id_raises_on_non_existent_stage_id(self):
        self.mock_staging_service.get_stage_order_by_id.return_value = None

        with self.assertRaises(InvalidStatusException):

            self.mover_delivery_service.deliver_by_staging_id(staging_id=1,
                                                              delivery_project='foo')

        pass

    def test_get_status_of_delivery_order(self):
        # TODO
        pass
