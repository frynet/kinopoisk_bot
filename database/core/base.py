from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# For alembic migrations
import database.dao  # noqa
