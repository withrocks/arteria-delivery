

import unittest


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from delivery.models.db_models import SQLAlchemyBase, StagingOrder, StagingStatus
from delivery.repositories.staging_repository import DatabaseBasedStagingRepository


class TestStagingRepository(unittest.TestCase):

    def setUp(self):
        # NOTE setting echo to true is very useful to se which sql statements get
        # executed, but since it fills up the logs a lot it's been disabled by
        # default here.
        engine = create_engine('sqlite:///:memory:', echo=False)
        SQLAlchemyBase.metadata.create_all(engine)

        # Throw some data into the in-memory db
        session_factory = sessionmaker()
        session_factory.configure(bind=engine)

        self.session = session_factory()

        self.staging_order_1 = StagingOrder(source='foo', status=StagingStatus.pending)
        self.session.add(self.staging_order_1)

        self.session.commit()

        # Prep the repo
        self.staging_repo = DatabaseBasedStagingRepository(session_factory)

    ###
    # A database backed staging repository should able to:
    # - get staging orders by source
    def test_get_staging_orders_by_source(self):
        actual = self.staging_repo.get_staging_order_by_source(self.staging_order_1.source)
        self.assertEqual(len(actual), 1)
        self.assertEqual(self.staging_order_1.id, actual[0].id)

    # - get staging orders by id
    def test_get_staging_orders_by_id(self):
        actual = self.staging_repo.get_staging_order_by_id(self.staging_order_1.id)
        self.assertEqual(self.staging_order_1.id, actual.id)

    # - create a new staging_order and persist it to the db
    def test_create_staging_order(self):
        order = self.staging_repo.create_staging_order(source='/foo', status=StagingStatus.pending)

        self.assertIsInstance(order, StagingOrder)
        self.assertEqual(order.status, StagingStatus.pending)
        self.assertEqual(order.id, 2)
        self.assertEqual(order.pid, None)
        self.assertEqual(order.source, '/foo')

        # Check that the object has been committed, i.e. there are no 'dirty' objects in session
        self.assertEqual(len(self.session.dirty), 0)
        order_from_session = self.session.query(
            StagingOrder).filter(StagingOrder.id == order.id).one()
        self.assertEqual(order_from_session.id, order.id)
