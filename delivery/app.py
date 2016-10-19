
from tornado.web import URLSpec as url

from arteria.web.app import AppService

from delivery.handlers.utility_handlers import VersionHandler
from delivery.handlers.runfolder_handlers import RunfolderHandler
from delivery.handlers.project_handlers import ProjectHandler, ProjectsForRunfolderHandler
from delivery.handlers.delivery_handlers import DeliverRunfolderHandler

from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository
from delivery.services.delivery_service import MoverDeliveryService
from delivery.services.external_program_service import ExternalProgramService


def routes(**kwargs):
    """
    Setup routes and feed them any kwargs passed, e.g.`routes(config=app_svc.config_svc)`
    Help will be automatically available at /api, and will be based on the
    doc strings of the get/post/put/delete methods
    :param: **kwargs will be passed when initializing the routes.
    """
    return [
        url(r"/api/1.0/version", VersionHandler, name="version", kwargs=kwargs),
        url(r"/api/1.0/runfolders", RunfolderHandler, name="runfolder", kwargs=kwargs),
        url(r"/api/1.0/projects", ProjectHandler, name="projects", kwargs=kwargs),
        url(r"/api/1.0/runfolder/(.+)/projects", ProjectsForRunfolderHandler,
            name="projects_for_runfolder", kwargs=kwargs),
        url(r"/api/1.0/deliver/runfolder/(.+)", DeliverRunfolderHandler,
            name="delivery_runfolder", kwargs=kwargs)
        # TODO Figure out if we want to be able to deliver any type of directory,
        # not just a runfolder
    ]


def start():
    """
    Start the delivery-ws app
    """
    app_svc = AppService.create(__package__)

    config = app_svc.config_svc
    runfolder_repo = FileSystemBasedRunfolderRepository(
        config["monitored_directory"])
    external_program_service = ExternalProgramService()
    delivery_service = MoverDeliveryService(external_program_service)

    app_svc.start(routes(config=config, runfolder_repo=runfolder_repo,
                         delivery_service=delivery_service))
