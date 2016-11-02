

import unittest


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from delivery.repositories.deliveries_repository import DatabaseBasedDeliveriesRepository
from delivery.models.deliveries import SQLAlchemyBase, StagingOrder, StagingStatus

from delivery.repositories.staging_repository import DatabaseBasedStagingRepository

class TestStagingRepository(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:', echo=True)
    repo = DatabaseBasedDeliveriesRepository(database_engine_handle=engine)

    SQLAlchemyBase.metadata.create_all(engine)

    # Throw some data into the in-memory db
    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    staging_order_1 = StagingOrder(source='foo', status=StagingStatus.pending)
    session.add(staging_order_1)

    session.commit()

    print session.query(StagingOrder).all()
    print session.dirty

    # Prep the repo
    staging_repo = DatabaseBasedStagingRepository(engine)

    def test_get_staging_orders_by_source(self):
        actual = self.staging_repo.get_staging_order_by_source(self.staging_order_1.source)
        self.assertEquals(self.staging_order_1, actual)


###
### A database backed staging repository should able to:
### - get staging orders by source
### - get staging orders by id
### - change state of a staging order to any permitted stage
### - associate a staging order with a pid