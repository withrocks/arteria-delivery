
import threading
import os

from delivery.models.deliveries import StagingStatus, StagingOrder
from delivery.exceptions import RunfolderNotFoundException,InvalidStatusException

class StagingService(object):

    # TODO On initiation of a Staging service, restart any ongoing stagings
    # since they should all have been killed.
    # And if we do so we need to make sure that the Staging service
    # acts as a singleton, look at: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    def __init__(self, staging_dir, external_program_service, staging_repo, runfolder_repo, session_factory):
        # TODO Figure our how to handle db session!
        self.staging_dir = staging_dir
        self.external_program_service = external_program_service
        self.staging_repo = staging_repo
        self.runfolder_repo = runfolder_repo
        self.session_factory = session_factory

    @staticmethod
    def _copy_dir(staging_order_id, external_program_service, staging_dir, session_factory, staging_repo):
        session = session_factory()

        # This is a somewhat hacky work-around to the problem that objects created in one
        # thread, and thus associated with another session cannot be accessed by another
        # thread, there fore it is re-materialized in here...
        staging_order = staging_repo.get_staging_order_by_id(staging_order_id, session)
        try:

            staging_target = os.path.join(staging_dir,
                                          "{}_{}".format(staging_order.id,
                                                         os.path.basename(staging_order.source)))

            cmd = ['rsync', '-r', staging_order.source, staging_target]

            execution = external_program_service.run(cmd)

            staging_order.pid = execution.pid
            session.commit()

            execution_result = external_program_service.wait_for_execution(execution)

            # TODO Add logging here..
            if execution_result.status_code == 0:
                staging_order.status = StagingStatus.staging_successful
                session.commit()
            else:
                staging_order.status = StagingStatus.staging_failed
                session.commit()

        # TODO Better exception handling here...
        except Exception as e:
            staging_order.status = StagingStatus.staging_failed
        finally:
            # Always commit the state change to the database
            session.commit()

    def stage_order(self, stage_order):

        session = self.session_factory()

        try:

            if stage_order.status != StagingStatus.pending:
                raise InvalidStatusException("Cannot start staging a delivery order with status: {}".
                                             format(stage_order.status))

            stage_order.status = StagingStatus.staging_in_progress
            session.commit()

            thread = threading.Thread(target=StagingService._copy_dir,
                                      kwargs={"staging_order_id": stage_order.id,
                                              "external_program_service": self.external_program_service,
                                              "staging_repo": self.staging_repo,
                                              "staging_dir": self.staging_dir,
                                              "session_factory": self.session_factory})

            # When only daemon threads remain, kill them and exit
            # This should hopefully mean that if the rest of the
            # application is terminated for some reason, there
            # should be no zombie threads left laying around...
            thread.setDaemon(True)
            thread.start()

        # TODO Better error handling
        except Exception as e:
            stage_order.status = StagingStatus.staging_failed
            session.commit()
            raise e

    def stage_runfolder(self, runfolder_id, projects_to_stage):

        runfolder = self.runfolder_repo.get_runfolder(runfolder_id)

        if not runfolder:
            raise RunfolderNotFoundException("Couldn't find runfolder matching: {}".format(runfolder_id))

        # If no projects have been specified, stage all projects
        if not projects_to_stage:
            projects_to_stage = runfolder.projects

        stage_order_ids = []
        for project in runfolder.projects:
            if project in projects_to_stage:

                # TODO Verify that there is no currently ongoing staging order before creating a new one...
                staging_order = self.staging_repo.create_staging_order(source=project.path,
                                                                       status=StagingStatus.pending)
                self.stage_order(staging_order)
                stage_order_ids.append(staging_order.id)

        return stage_order_ids


