
from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler


class RunfolderBaseHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        super(RunfolderBaseHandler, self).initialize(kwargs)


class RunfolderHandler(RunfolderBaseHandler):
    """
    Get all runfolders
    """

    def initialize(self, **kwargs):
        super(RunfolderHandler, self).initialize(**kwargs)

    def get(self):
        """
        Returns all runfolders
        """
        runfolders = list(self.runfolder_repo.get_runfolders())
        self.write_list_of_models_as_json(runfolders, key="runfolders")
