
from arteria.web.handlers import BaseRestHandler

from delivery import __version__ as version


class ArteriaDeliveryBaseHandler(BaseRestHandler):
    """
    Base handler for checksum.
    """

    def initialize(self, config):
        """
        Ensures that any parameters feed to this are available
        to subclasses.

        :param: config configuration used by the service
        """
        self.config = config


class VersionHandler(ArteriaDeliveryBaseHandler):

    """
    Get the version of the service
    """

    def get(self):
        """
        Returns the version of the checksum-service
        """
        self.write_object({"version": version})
