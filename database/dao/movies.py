from datetime import datetime, UTC

from sqlalchemy import Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from api.kinopoisk.dto.movie import MovieType
from database.core.base import Base
from database.core.types.movie_genre import GenreListType


class MovieDao(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kinopoisk_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)

    name: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    type: Mapped[MovieType | None] = mapped_column(Enum(MovieType, native_enum=False))

    year: Mapped[int | None] = mapped_column(Integer)
    age_rating: Mapped[int | None] = mapped_column(Integer)
    poster_url: Mapped[str | None] = mapped_column(String)

    rating_kp: Mapped[float | None] = mapped_column(Float)
    rating_imdb: Mapped[float | None] = mapped_column(Float)

    budget_value: Mapped[float | None] = mapped_column(Float)
    budget_currency: Mapped[str | None] = mapped_column(String(8))

    genres: Mapped[list[str]] = mapped_column(
        GenreListType,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
