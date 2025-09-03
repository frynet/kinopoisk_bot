from __future__ import annotations

from datetime import datetime, UTC

from sqlalchemy import Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core.base import Base
from database.dao import UserDao
from database.dao.movies import MovieDao


class UserMovieSearchLog(Base):
    __tablename__ = "users_movies_search_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        index=True,
    )

    user: Mapped[UserDao] = relationship()
    movie: Mapped[MovieDao] = relationship()


Index(
    "ix_users_movies_search_log_user_time",
    UserMovieSearchLog.user_id,
    UserMovieSearchLog.timestamp.desc(),
)
