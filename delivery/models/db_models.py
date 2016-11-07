
from sqlalchemy import Column, Integer, String, Enum
import enum as base_enum


from sqlalchemy.ext.declarative import declarative_base

SQLAlchemyBase = declarative_base()


class StagingStatus(base_enum.Enum):

    pending = 'pending'

    staging_in_progress = 'staging_in_progress'
    staging_successful = 'staging_successful'
    staging_failed = 'staging_failed'


class StagingOrder(SQLAlchemyBase):

    __tablename__ = 'staging_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    status = Column(Enum(StagingStatus), nullable=False)
    pid = Column(Integer)

    def __repr__(self):
        return "Staging order: {id: %s, source: %s, status: %s, pid: %s }" % (str(self.id),
                                                                              self.source,
                                                                              self.status,
                                                                              self.pid)


class DeliveryIdentifier(object):
    # TODO Evaluate if we should use this or not, depends on how Mover will work

    def __init__(self, identifier):
        self.id = identifier


class DeliveryStatus(base_enum.Enum):

    pending = 'pending'

    delivery_in_progress = 'delivery_in_progress'
    delivery_finished = 'delivery_successful'
    delivery_failed = 'delivery_failed'


class DeliveryOrder(SQLAlchemyBase):

    __tablename__ = 'delivery_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_source = Column(String, nullable=False)
    delivery_project = Column(String, nullable=False)
    delivery_status = Column(Enum(DeliveryStatus))

    def __repr__(self):
        return "Delivery order: {id: %s, source: %s, project: %s, status: %s }" % (str(self.id),
                                                                                   self.delivery_source,
                                                                                   self.delivery_project,
                                                                                   self.delivery_status)
