from sqlalchemy.orm import sessionmaker

from delivery.models.db_models import DeliveryOrder


class BaseDeliveriesRepository(object):
    """
    Provides interface that needs to be supported by all subclasses
    """

    def get_delivery_orders_for_source(self, source_directory):
        raise NotImplementedError("Must be implemented by subclass")

    def get_ongoing_delivery_order_for_source(self, source_directory):
        raise NotImplementedError("Must be implemented by subclass")

    def get_delivery_order_by_id(self, delivery_order_id):
        raise NotImplementedError("Must be implemented by subclass")

    def get_delivery_orders(self):
        raise NotImplementedError("Must be implemented by subclass")

    def add_delivery_order(self, delivery_order):
        raise NotImplementedError("Must be implemented by subclass")


class DatabaseBasedDeliveriesRepository(BaseDeliveriesRepository):

    def __init__(self, session_factory):
        self.session = session_factory()

    def get_delivery_orders_for_source(self, source_directory):
        return self.session.query(DeliveryOrder).filter(DeliveryOrder.delivery_source == source_directory).all()

    def get_delivery_order_by_id(self, delivery_order_id):
        return self.session.query(DeliveryOrder).filter(DeliveryOrder.id == delivery_order_id).one()

    def get_delivery_orders(self):
        return self.session.query(DeliveryOrder).all()

    def create_delivery_order(self, delivery_source, delivery_project, delivery_status, staging_order_id):
        """

        :param delivery_source: the source directory to be delivered
        :param delivery_project: the project code for the project to deliver to
        :param delivery_status: status of the delivery
        :param staging_order_id: NOTA BENE: this will need to be verified against the staging table before
                                 inserting it here, because at this point there is no validation that the
                                 value is valid!
        :return: the created delivery order
        """
        order = DeliveryOrder(delivery_source=delivery_source,
                              delivery_project=delivery_project,
                              delivery_status=delivery_status,
                              staging_order_id=staging_order_id)
        self.session.add(order)
        self.session.commit()

        return order


