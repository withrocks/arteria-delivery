import unittest
import mock
import time
import random


from delivery.exceptions import InvalidStatusException
from delivery.services.staging_service import StagingService
from delivery.models.deliveries import StagingOrder,StagingStatus
from delivery.models.execution import ExecutionResult,Execution


class TestStagingService(unittest.TestCase):

    class MockExternalRunnerService():

        @staticmethod
        def run(cmd):
            mock_process = mock.MagicMock()
            execution = Execution(pid=random.randint(1, 1000), process_obj=mock_process)
            return execution

        @staticmethod
        def wait_for_execution(execution):
            time.sleep(0.1)
            return ExecutionResult(status_code=0,
                                   stderr="stderr",
                                   stdout="stdout")

    staging_order1 = StagingOrder(source='/test/this',
                                  status=StagingStatus.pending)

    mock_external_runner_service = MockExternalRunnerService()
    mock_staging_repo = mock.MagicMock()
    mock_staging_repo.get_staging_order_by_id.return_value = staging_order1

    mock_runfolder_repo = mock.MagicMock()
    mock_db_session_factory = mock.MagicMock()

    staging_service = StagingService("/tmp",
                                     mock_external_runner_service,
                                     mock_staging_repo,
                                     mock_runfolder_repo,
                                     mock_db_session_factory)

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

    ### A StagingService should be able to:
    ### - Stage a staging order
    def test_stage_order(self):
        self.staging_service.stage_order(stage_order=self.staging_order1)
        def _get_stating_status():
            return self.staging_order1.status

        self._eventually_equals(1, _get_stating_status, StagingStatus.staging_successful)

    ### - Reject staging order if it has invalid state
    def test_stage_order_non_valid_state(self):
        with self.assertRaises(InvalidStatusException):

            staging_order_in_progress = StagingOrder(source='/test/this',
                                                     status=StagingStatus.staging_in_progress)

            self.staging_service.stage_order(stage_order=staging_order_in_progress)


    ### - Be able to stage a existing runfolder
    def test_stage_runfolder(self):
        pass

    ### - Reject staging a runfolder which does not exist runfolder
    def test_stage_runfolder(self):
        pass
