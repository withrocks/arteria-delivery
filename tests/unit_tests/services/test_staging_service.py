import unittest
import mock
import time
import random
import signal

from delivery.exceptions import InvalidStatusException, RunfolderNotFoundException
from delivery.services.staging_service import StagingService
from delivery.models.db_models import StagingOrder, StagingStatus
from delivery.models.execution import ExecutionResult, Execution
from tests.test_utils import FAKE_RUNFOLDERS, assert_eventually_equals


class TestStagingService(unittest.TestCase):

    class MockExternalRunnerService():

        def __init__(self, return_status=0, throw=False):
            self.return_status = return_status
            self.throw = throw

        def run(self, cmd):
            if self.throw:
                raise Exception("Test the exception handling...")
            mock_process = mock.MagicMock()
            execution = Execution(pid=random.randint(1, 1000), process_obj=mock_process)
            return execution

        def wait_for_execution(self, execution):
            time.sleep(0.1)
            return ExecutionResult(status_code=self.return_status,
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

    # A StagingService should be able to:
    # - Stage a staging order
    def test_stage_order(self):
        self.staging_service.stage_order(stage_order=self.staging_order1)

        def _get_stating_status():
            return self.staging_order1.status

        assert_eventually_equals(self, 1, _get_stating_status, StagingStatus.staging_successful)

    # - Set status to failed if rsyncing is not successful
    def test_unsuccessful_staging_order(self):
        mock_external_runner_service = self.MockExternalRunnerService(return_status=1)
        self.staging_service.external_program_service = mock_external_runner_service

        self.staging_service.stage_order(stage_order=self.staging_order1)

        def _get_stating_status():
            return self.staging_order1.status

        assert_eventually_equals(self, 1, _get_stating_status, StagingStatus.staging_failed)

    # - Set status to failed if there is an exception is not successful
    def test_exception_in_staging_order(self):
        mock_external_runner_service = self.MockExternalRunnerService(throw=True)
        self.staging_service.external_program_service = mock_external_runner_service

        self.staging_service.stage_order(stage_order=self.staging_order1)

        def _get_stating_status():
            return self.staging_order1.status

        assert_eventually_equals(self, 1, _get_stating_status, StagingStatus.staging_failed)

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

            def create_staging_order(self, source, status, staging_target_dir):

                order = StagingOrder(id=len(self.orders_state) + 1,
                                     source=source,
                                     status=status,
                                     staging_target=staging_target_dir)
                self.orders_state.append(order)
                return order

        runfolder1 = FAKE_RUNFOLDERS[0]

        self.mock_runfolder_repo.get_runfolder.return_value = runfolder1
        mock_staging_repo = MockStagingRepo()

        self.staging_service.staging_repo = mock_staging_repo

        result = self.staging_service.stage_runfolder(
            runfolder_id=runfolder1.name, projects_to_stage=[])
        self.assertEqual(result, map(lambda x: x.id, mock_staging_repo.orders_state))

    # - Reject staging a runfolder which does not exist runfolder
    def test_stage_runfolder_does_not_exist(self):
        with self.assertRaises(RunfolderNotFoundException):

            self.mock_runfolder_repo.get_runfolder.return_value = None
            self.staging_service.stage_runfolder(runfolder_id='foo_runfolder', projects_to_stage=[])

    # - Be able to get the status of a stage order
    def test_get_status_or_stage_order(self):
        # Returns correctly for existing order
        actual = self.staging_service.get_status_of_stage_order(self.staging_order1.id)
        self.assertEqual(actual, self.staging_order1.status)

        # Returns None for none existent order
        mock_staging_repo = mock.MagicMock()
        mock_staging_repo.get_staging_order_by_id.return_value = None
        self.staging_service.staging_repo = mock_staging_repo
        actual_not_there = self.staging_service.get_status_of_stage_order(1337)
        self.assertIsNone(actual_not_there)

    # - Be able to kill a ongoing staging process
    @mock.patch('delivery.services.staging_service.os')
    def test_kill_stage_order(self, mock_os):

        # If the status is in progress it should be possible to kill it.
        self.staging_order1.status = StagingStatus.staging_in_progress
        self.staging_order1.pid = 1337
        actual = self.staging_service.kill_process_of_staging_order(self.staging_order1.id)
        mock_os.kill.assert_called_with(self.staging_order1.pid, signal.SIGTERM)
        self.assertTrue(actual)

        # It should handle if kill raises a OSError gracefully
        self.staging_order1.status = StagingStatus.staging_in_progress
        self.staging_order1.pid = 1337
        mock_os.kill.side_effect = OSError
        actual = self.staging_service.kill_process_of_staging_order(self.staging_order1.id)
        mock_os.kill.assert_called_with(self.staging_order1.pid, signal.SIGTERM)
        self.assertFalse(actual)

        # If the status is not in progress it should not be possible to kill it.
        self.staging_order1.status = StagingStatus.staging_successful
        actual = self.staging_service.kill_process_of_staging_order(self.staging_order1.id)
        mock_os.kill.assert_not_called()
        self.assertFalse(actual)
