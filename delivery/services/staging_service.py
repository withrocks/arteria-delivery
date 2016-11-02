
import threading
import os

from delivery.models.deliveries import StagingStatus


class StagingService(object):

    # TODO On initiation of a Staging service, restart any ongoing stagings
    # since they should all have been killed.
    # And if we do so we need to make sure that the Staging service
    # acts as a singleton, look at: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    def __init__(self, staging_dir, external_program_service):
        self.staging_dir = staging_dir
        self.external_program_service = external_program_service

    @staticmethod
    def _copy_dir(delivery_order, external_program_service, staging_dir):
        try:

            staging_target = os.path.join(staging_dir,
                                          "{}_{}".format(os.path.basename(delivery_order.delivery_source),
                                                         delivery_order.delivery_project))

            cmd = ['rsync', '-r', delivery_order.delivery_source, staging_target]
            execution_result = external_program_service.run_and_wait(cmd)

            # TODO Add logging here..
            if execution_result.status_code == 0:
                delivery_order.delivery_status = StagingStatus.staging_successful
            else:
                delivery_order.delivery_status = StagingStatus.delivery_failed

        # TODO Better exception handling here...
        except Exception as e:
            delivery_order.delivery_status = StagingStatus.delivery_failed
            raise e

    def stage_order(self, delivery_order):

        if delivery_order.delivery_status == StagingStatus.pending:
            delivery_order.delivery_status = StagingStatus.staging_in_progress

            thread = threading.Thread(target=StagingService._copy_dir,
                                      kwargs={"delivery_order": delivery_order,
                                              "external_program_service": self.external_program_service,
                                              "staging_dir": self.staging_dir})

            # When only daemon threads remain, kill them and exit
            # This should hopefully mean that if the rest of the
            # application is terminated for some reason, there
            # should be no zombie threads left laying around...
            thread.setDaemon(True)
            thread.start()
        else:
            # TODO Better exception here!
            raise Exception("Cannot start staging a delivery order with status: {}".
                            format(delivery_order.delivery_status))
