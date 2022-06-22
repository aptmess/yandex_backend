from contextlib import contextmanager
from typing import Any, Iterator

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.config import config

engine = sa.create_engine(config.DATABASE_URL, echo=True)


local_session = sessionmaker(bind=engine)


@contextmanager
def create_session() -> Iterator[Any]:
    new_session = local_session()
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


def get_session() -> Any:
    with create_session() as s:
        yield s
