import unittest
from delivery.services.staging_service import StagingService
import time
from delivery.models.deliveries import DeliveryOrder,StagingStatus
from delivery.models.execution import ExecutionResult


class TestStagingService(unittest.TestCase):

    class MockExternalRunnerService():
        def run_and_wait(self, cmd):
            time.sleep(0.1)
            return ExecutionResult(status_code=0,
                                   stderr="stderr",
                                   stdout="stdout")

    staging_service = StagingService("/tmp", MockExternalRunnerService())

    def _eventually_equals(self, timeout, f, expected, delay=0.1):
        start_time = time.time()

        while True:
            try:
                value = f()
                self.assertEquals(value, expected)
                break
            except AssertionError:
                if time.time() - start_time <= timeout:
                    time.sleep(delay)
                    continue
                else:
                    raise

    def test_stage_order(self):
        delivery_order1 = DeliveryOrder(delivery_source='/test/this',
                                        delivery_project='b201782',
                                        delivery_status=StagingStatus.pending)

        self.staging_service.stage_order(delivery_order=delivery_order1)
        def _get_delivery_status():
            return delivery_order1.delivery_status

        self._eventually_equals(1, _get_delivery_status, StagingStatus.staging_successful)

    def test_stage_order_non_valid_state(self):
        with self.assertRaises(Exception):
            delivery_order1 = DeliveryOrder(delivery_source='/test/this',
                                            delivery_project='b201782',
                                            delivery_status=DeliveryStatus.delivery_in_progress)

            self.staging_service.stage_order(delivery_order=delivery_order1)
