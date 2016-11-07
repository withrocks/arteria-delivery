
import logging
import threading
import os
import signal

from delivery.models.db_models import StagingStatus
from delivery.exceptions import RunfolderNotFoundException, InvalidStatusException

log = logging.getLogger(__name__)


class StagingService(object):

    # TODO On initiation of a Staging service, restart any ongoing stagings
    # since they should all have been killed.
    # And if we do so we need to make sure that the Staging service
    # acts as a singleton, look at:
    # http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    def __init__(self, staging_dir, external_program_service, staging_repo, runfolder_repo, session_factory):
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

            if execution_result.status_code == 0:
                staging_order.status = StagingStatus.staging_successful
                session.commit()
                log.info("Successfully staged: {}".format(staging_order))
            else:
                staging_order.status = StagingStatus.staging_failed
                session.commit()
                log.info("Failed in staging: {} because rsync returned exit code: {}".
                         format(staging_order, execution_result.status_code))

        # TODO Better exception handling here...
        except Exception as e:
            staging_order.status = StagingStatus.staging_failed
            log.info("Failed in staging: {} because this exception was logged: {}".
                     format(staging_order, e))
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
            raise RunfolderNotFoundException(
                "Couldn't find runfolder matching: {}".format(runfolder_id))

        # If no projects have been specified, stage all projects
        if not projects_to_stage:
            projects_to_stage = runfolder.projects

        stage_order_ids = []
        for project in runfolder.projects:
            if project in projects_to_stage:
                # TODO Verify that there is no currently ongoing staging order before
                # creating a new one...
                staging_order = self.staging_repo.create_staging_order(source=project.path,
                                                                       status=StagingStatus.pending)
                log.debug("Created a staging order: {}".format(staging_order))
                self.stage_order(staging_order)
                stage_order_ids.append(staging_order.id)

        return stage_order_ids

    def get_status_of_stage_order(self, stage_order_id):
        stage_order = self.staging_repo.get_staging_order_by_id(stage_order_id)
        if stage_order:
            return stage_order.status
        else:
            return None

    def kill_process_of_staging_order(self, stage_order_id):
        """
        Attempt to kill the process of the stage order.
        Will only kill stage orders which have a 'staging_in_progress' status.
        :param stage_order_id:
        :return: True if the process was killed successfully, otherwise False
        """
        session = self.session_factory()
        stage_order = self.staging_repo.get_staging_order_by_id(stage_order_id, session)

        if not stage_order:
            return False

        try:
            if stage_order.status != StagingStatus.staging_in_progress:
                raise InvalidStatusException(
                    "Can only kill processes where the staging order is 'staging_in_progress'")

            os.kill(stage_order.pid, signal.SIGTERM)

        except OSError:
            log.error("Failed to kill process with pid: {} associated with staging order: {} ".
                      format(stage_order.id, stage_order.pid))
            return False
        except InvalidStatusException:
            log.warning("Tried to kill process for staging order: {}, but didn't to it because it's status did not make"
                        "it eligible for killing.".format(stage_order.id))
            return False
        else:
            log.debug("Successfully killed process with pid: {} associated with staging order: {} ".
                      format(stage_order.id, stage_order.pid))
            stage_order.status = StagingStatus.staging_failed
            session.commit()
            return True
