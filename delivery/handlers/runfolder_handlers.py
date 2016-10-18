
from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler


class RunfolderHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        super(RunfolderHandler, self).initialize(kwargs)

    """
    Get all runfolders
    """

    def get(self):
        """
        Returns all runfolders
        """
        runfolders_as_json = map(lambda x: x.to_json(), list(
            self.runfolder_repo.get_runfolders()))
        self.write_json({"runfolders": runfolders_as_json})
