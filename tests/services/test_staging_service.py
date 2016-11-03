import unittest
import mock
import time
import random


from delivery.exceptions import InvalidStatusException, RunfolderNotFoundException
from delivery.services.staging_service import StagingService
from delivery.models.deliveries import StagingOrder, StagingStatus
from delivery.models.execution import ExecutionResult, Execution
from tests.test_utils import FAKE_RUNFOLDERS


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

    def setUp(self):
        self.staging_order1 = StagingOrder(id=1,
                                           source='/test/this',
                                           status=StagingStatus.pending)

        mock_external_runner_service = self.MockExternalRunnerService()
        mock_staging_repo = mock.MagicMock()
        mock_staging_repo.get_staging_order_by_id.return_value = self.staging_order1
        mock_staging_repo.create_staging_order.return_value = self.staging_order1

        self.mock_runfolder_repo = mock.MagicMock()

        mock_db_session_factory = mock.MagicMock()

        self.staging_service = StagingService("/tmp",
                                              mock_external_runner_service,
                                              mock_staging_repo,
                                              self.mock_runfolder_repo,
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

    # A StagingService should be able to:
    # - Stage a staging order
    def test_stage_order(self):
        self.staging_service.stage_order(stage_order=self.staging_order1)
        def _get_stating_status():
            return self.staging_order1.status

        self._eventually_equals(1, _get_stating_status, StagingStatus.staging_successful)

    # - Reject staging order if it has invalid state
    def test_stage_order_non_valid_state(self):
        with self.assertRaises(InvalidStatusException):

            staging_order_in_progress = StagingOrder(source='/test/this',
                                                     status=StagingStatus.staging_in_progress)

            self.staging_service.stage_order(stage_order=staging_order_in_progress)

    # - Be able to stage a existing runfolder
    def test_stage_runfolder(self):

        class MockStagingRepo:

            orders_state = []

            def get_staging_order_by_id(self, identifier, custom_session=None):
                return filter(lambda x: x.id == identifier, self.orders_state)[0]

            def create_staging_order(self, source, status):

                order = StagingOrder(id=len(self.orders_state)+1, source=source, status=status)
                self.orders_state.append(order)
                return order

        runfolder1 = FAKE_RUNFOLDERS[0]

        mock_external_runner_service = self.MockExternalRunnerService()
        mock_staging_repo = MockStagingRepo()

        mock_runfolder_repo = mock.MagicMock()
        mock_runfolder_repo.get_runfolder.return_value = runfolder1

        mock_db_session_factory = mock.MagicMock()

        staging_service = StagingService("/tmp",
                                         mock_external_runner_service,
                                         mock_staging_repo,
                                         mock_runfolder_repo,
                                         mock_db_session_factory)

        result = staging_service.stage_runfolder(runfolder_id=runfolder1.name, projects_to_stage=[])
        self.assertEqual(result, map(lambda x: x.id, mock_staging_repo.orders_state))


    # - Reject staging a runfolder which does not exist runfolder
    def test_stage_runfolder_does_not_exist(self):
        with self.assertRaises(RunfolderNotFoundException):

            self.mock_runfolder_repo.get_runfolder.return_value = None
            self.staging_service.stage_runfolder(runfolder_id='foo_runfolder', projects_to_stage=[])

