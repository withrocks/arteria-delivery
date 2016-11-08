
import os

from sqlalchemy.orm.exc import NoResultFound

from delivery.models.db_models import StagingOrder


class DatabaseBasedStagingRepository(object):
    """
    A repository of staging orders backed by a database. It is able to create and commit new staging orders
    to the database, and fetch them based on different factors.
    """

    def __init__(self, session_factory):
        """
        Instantiate a new DatabaseBasedStagingRepository
        :param session_factory: factory method which can produce new sqlalchemy Session objects
        """
        self.session = session_factory()

    def get_staging_order_by_source(self, source):
        """
        Get all staging orders based on their source
        :param source: to search for
        :return: All staging orders of that source as a list
        """
        return self.session.query(StagingOrder).filter(StagingOrder.source == source).all()

    def get_staging_order_by_id(self, identifier, custom_session=None):
        """
        Get a staging order by id
        NOTE
        The custom_session used here is used because in the `StagingService` it is necessary to
        make this query from a separate thread, something which sqlalchemy does not allow. Therefore
        I've made it possible to provide a separate session here (in that case a new session instantiate in the
        thread), while hacky it appears to work. /JD 20161108
        :param identifier: the stating order id to search for
        :param custom_session: provide an other session object if that is neccessary for your use case.
        :return: the matching StagingOrder or None, if there was no matching stating order.
        """
        if custom_session:
            session = custom_session
        else:
            session = self.session
        try:
            return session.query(StagingOrder).filter(StagingOrder.id == identifier).one()
        except NoResultFound:
            return None

    def create_staging_order(self, source, status, staging_target_dir):
        """
        Create a StatingOrder and commit it to the database
        :param source: the directory or file to stage
        :param status: the initial StatingStatus to assign to the StatingORder
        :param staging_target_dir: the directory to which the StagingOrder should transfer the source
        :return:
        """

        order = StagingOrder(source=source, status=status)
        self.session.add(order)

        self.session.commit()

        staging_target = os.path.join(staging_target_dir,
                                      "{}_{}".format(order.id,
                                                     os.path.basename(order.source)))

        order.staging_target = staging_target
        self.session.commit()

        return order
