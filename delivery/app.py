
from tornado.web import URLSpec as url

from arteria.web.app import AppService

from delivery.handlers.utility_handlers import VersionHandler
from delivery.handlers.runfolder_handlers import RunfolderHandler
from delivery.handlers.project_handlers import ProjectHandler

from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository


def routes(**kwargs):
    """
    Setup routes and feed them any kwargs passed, e.g.`routes(config=app_svc.config_svc)`
    Help will be automatically available at /api, and will be based on the
    doc strings of the get/post/put/delete methods
    :param: **kwargs will be passed when initializing the routes.
    """
    return [
        url(r"/api/1.0/version", VersionHandler, name="version", kwargs=kwargs),
        url(r"/api/1.0/runfolders", RunfolderHandler,
            name="runfolder", kwargs=kwargs),
        url(r"/api/1.0/projects", ProjectHandler,
            name="projects", kwargs=kwargs)
    ]


def start():
    """
    Start the delivery-ws app
    """
    app_svc = AppService.create(__package__)

    config = app_svc.config_svc
    runfolder_repo = FileSystemBasedRunfolderRepository(
        config["monitored_directory"])

    app_svc.start(routes({"config": config, "runfolder_repo": runfolder_repo}))
