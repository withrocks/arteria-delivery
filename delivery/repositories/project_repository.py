

class FileSystemBasedProjectRepository(object):

    def __init__(self, runfolder_repository):
        self.runfolder_repository = runfolder_repository

    def get_projects(self):
        for runfolder in self.runfolder_repository.get_runfolders():
            for project in runfolder.projects:
                yield project

