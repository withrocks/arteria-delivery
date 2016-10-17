
import json

from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler

from delivery.repositories.runfolder_repository import FileSystemBasedRunfolderRepository


class RunfolderHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        # TODO Don't know if this should be called here, or if __init__ method should be used
        self.runfolder_repo = kwargs["runfolder_repo"]
        super(RunfolderHandler, self).initialize(kwargs)

    """
    Get all runfolders
    """
    def get(self):
        """
        Returns all runfolders
        """
        runfolders_as_json = map(lambda x: x.to_json(), list(self.runfolder_repo.get_runfolders()))
        self.write_json({"runfolders": runfolders_as_json})
