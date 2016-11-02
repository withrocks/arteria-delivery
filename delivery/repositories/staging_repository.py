from sqlalchemy.orm import sessionmaker

from delivery.models.deliveries import DeliveryOrder


class BaseStagingRepository(object):
    """
    Provides interface that needs to be supported by all subclasses
    """

    def get_staging_order_by_source(self, source):
        raise NotImplementedError("Has to be implemented by subclass")

    def get_staging_order_by_id(self, identifier):
        raise NotImplementedError("Has to be implemented by subclass")

    def set_state_of_staging_order(self, staging_order, new_state):
        raise NotImplementedError("Has to be implemented by subclass")

    def set_pid_of_staging_order(self, staging_order, pid):
        raise NotImplementedError("Has to be implemented by subclass")


class DatabaseBasedStagingRepository(BaseStagingRepository):

    def __init__(self, database_engine_handle):
        self.db_handle = database_engine_handle

    def _get_session(self):
        Session = sessionmaker(self.db_handle)
        return Session()

    def get_staging_order_by_source(self, source):
        session = self._get_session()
        return session.query(DeliveryOrder).filter(DeliveryOrder.delivery_source == source).all()

    def get_staging_order_by_id(self, identifier):
        raise NotImplementedError("Has to be implemented by subclass")

    def set_state_of_staging_order(self, staging_order, new_state):
        raise NotImplementedError("Has to be implemented by subclass")

    def set_pid_of_staging_order(self, staging_order, pid):
        raise NotImplementedError("Has to be implemented by subclass")
