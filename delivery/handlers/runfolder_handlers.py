
from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler


class RunfolderBaseHandler(ArteriaDeliveryBaseHandler):
    """
    Base handler for handlers concerned with runfolders.
    """

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        super(RunfolderBaseHandler, self).initialize(kwargs)


class RunfolderHandler(RunfolderBaseHandler):
    """
    Manage runfolder resources
    """

    def initialize(self, **kwargs):
        super(RunfolderHandler, self).initialize(**kwargs)

    def get(self):
        """
        Returns all runfolders as json on the following format:
        {
            "runfolders": [
                {
                    "path": "/home/MOLMED/johda411/workspace/arteria/arteria-delivery/tests/resources/160930_ST-E00216_0111_BH37CWALXX",
                    "name": "160930_ST-E00216_0111_BH37CWALXX",
                    "projects": [
                        {
                            "path": "/home/MOLMED/johda411/workspace/arteria/arteria-delivery/tests/resources/160930_ST-E00216_0111_BH37CWALXX/Projects/ABC_123",
                            "name": "ABC_123",
                            "runfolder_path": "/home/MOLMED/johda411/workspace/arteria/arteria-delivery/tests/resources/160930_ST-E00216_0111_BH37CWALXX"
                        }
                    ]
                }
            ]
        }
        """
        runfolders = list(self.runfolder_repo.get_runfolders())
        self.write_list_of_models_as_json(runfolders, key="runfolders")
