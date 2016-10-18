
import json

from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler
from delivery.repositories.project_repository import ProjectRepository


class ProjectHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        self.project_repo = ProjectRepository(
            runfolder_repository=self.runfolder_repo)
        super(ProjectHandler, self).initialize(kwargs)

    """
    Get all projects
    """

    def get(self):
        """
        Returns all projects
        """
        projects_as_json = map(lambda x: x.to_json(), list(
            self.project_repo.get_projects()))
        self.write_json({"projects": projects_as_json})
