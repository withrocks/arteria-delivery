
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
import enum as base_enum


SQLAlchemyBase = declarative_base()


class DeliveryIdentifier(object):
    # TODO Evaluate if we should use this or not, depends on how Mover will work

    def __init__(self, identifier):
        self.id = identifier


class DeliveryStatus(base_enum.Enum):

    pending = 'pending'
    staging = 'staging'
    delivering = 'delivering'
    successful = 'successful'
    failed = 'failed'


class DeliveryOrder(SQLAlchemyBase):

    __tablename__ = 'delivery_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_target = Column(String)
    delivery_project = Column(String)
    delivery_status = Column(Enum(DeliveryStatus))

    def __repr__(self):
        return "Delivery order: {id: %s, target: %s, project: %s, status: %s }" % (str(self.id),
                                                                                   self.delivery_target,
                                                                                   self.delivery_project,
                                                                                   self.delivery_status)
