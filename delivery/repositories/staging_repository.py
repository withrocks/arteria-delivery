
from delivery.models.deliveries import StagingOrder


class BaseStagingRepository(object):
    """
    Provides interface that needs to be supported by all subclasses
    """

    def get_staging_order_by_source(self, source):
        raise NotImplementedError("Has to be implemented by subclass")

    def get_staging_order_by_id(self, identifier):
        raise NotImplementedError("Has to be implemented by subclass")

    def create_staging_order(self, source, status):
        raise NotImplementedError("Has to be implemented by subclass")


class DatabaseBasedStagingRepository(BaseStagingRepository):

    def __init__(self, session):
        self.session = session

    def get_staging_order_by_source(self, source):
        return self.session.query(StagingOrder).filter(StagingOrder.source == source).all()

    def get_staging_order_by_id(self, identifier):
        return self.session.query(StagingOrder).filter(StagingOrder.id == identifier).one()

    def create_staging_order(self, source, status):
        order = StagingOrder(source=source, status=status)
        self.session.add(order)
        self.session.commit()
        return order
