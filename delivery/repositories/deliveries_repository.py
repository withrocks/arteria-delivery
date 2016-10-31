from sqlalchemy.orm import sessionmaker

from delivery.models.deliveries import DeliveryOrder


class BaseDeliveriesRepository(object):
    """
    Provides interface that needs to be supported by all subclasses
    """

    def get_delivery_order(self, delivery_order_id):
        raise NotImplementedError("Must be implemented by subclass")

    def get_delivery_orders(self):
        raise NotImplementedError("Must be implemented by subclass")

    def add_delivery_order(self, delivery_order):
        raise NotImplementedError("Must be implemented by subclass")


class DatabaseBasedDeliveriesRepository(BaseDeliveriesRepository):

    def __init__(self, database_engine_handle):
        self.db_handle = database_engine_handle

    def _get_session(self):
        Session = sessionmaker(self.db_handle)
        return Session()

    def get_delivery_order(self, delivery_order_id):
        session = self._get_session()
        return session.query(DeliveryOrder).filter(DeliveryOrder.id == delivery_order_id).one()

    def get_delivery_orders(self):
        session = self._get_session()
        return session.query(DeliveryOrder).all()

    def add_delivery_order(self, delivery_order):
        session = self._get_session()
        session.add(delivery_order)
        # TODO Probably need to do transaction handling here...
        session.commit()
        # TODO How to handle returns here?
