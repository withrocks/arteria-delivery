
from delivery.handlers.utility_handlers import ArteriaDeliveryBaseHandler
from delivery.repositories.project_repository import ProjectRepository


class ProjectBaseHandler(ArteriaDeliveryBaseHandler):

    def initialize(self, **kwargs):
        self.runfolder_repo = kwargs["runfolder_repo"]
        self.project_repo = ProjectRepository(
            runfolder_repository=self.runfolder_repo)
        super(ProjectBaseHandler, self).initialize(kwargs)


class ProjectHandler(ProjectBaseHandler):
    """
    Get all projects
    """

    def get(self):
        """
        Returns all projects
        """
        projects = list(self.project_repo.get_projects())
        self.write_list_of_models_as_json(projects, key="projects")


class ProjectsForRunfolderHandler(ProjectBaseHandler):

    def get(self, runfolder_name):
        runfolder = self.runfolder_repo.get_runfolder(runfolder_name)
        if runfolder:
            projects = runfolder.projects
            self.write_list_of_models_as_json(projects, key="projects")
        else:
            self.send_error(status_code=404)
