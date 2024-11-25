import tenacity
import sqlalchemy

from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .user.model import User, CartItem
from .item.model import Item


def create_db_schema():
    _wait_for_db(engine)
    Base.metadata.create_all(bind=engine)


@tenacity.retry(
    stop=tenacity.stop_after_delay(10), wait=tenacity.wait_fixed(0.2), reraise=True
)
def _wait_for_db(sql_engine: sqlalchemy.Engine):
    with sql_engine.connect():
        pass
