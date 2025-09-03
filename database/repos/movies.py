from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from api.kinopoisk.dto.movie import MovieDto
from ..dao.movies import MovieDao


class MovieRepository:

    @classmethod
    def _dto_to_values(cls, dto) -> dict | None:
        data = dto.model_dump(by_alias=True)

        if not (kinopoisk_id := data.get("id")):
            return None

        poster = data.get("poster") or {}
        rating = data.get("rating") or {}
        budget = data.get("budget") or {}
        movie_type = getattr(data.get("type"), "value", data.get("type"))
        genres = [
            genre["name"]
            for genre in (data.get("genres") or [])
            if "name" in genre
        ]

        return {
            "kinopoisk_id": kinopoisk_id,
            "name": data.get("name"),
            "description": data.get("description"),
            "year": data.get("year"),
            "genres": genres,
            "age_rating": data.get("ageRating"),
            "poster_url": str(url) if (url := poster.get("url")) else None,
            "rating_kp": rating.get("kp"),
            "rating_imdb": rating.get("imdb"),
            "type": movie_type,
            "budget_value": budget.get("value"),
            "budget_currency": budget.get("currency"),
        }

    @classmethod
    def upsert_movie(
            cls,
            session: Session,
            dto: MovieDto,
    ) -> MovieDao | None:
        if not (values := cls._dto_to_values(dto)):
            return None

        stmt = insert(MovieDao).values(values).on_conflict_do_update(
            index_elements=[MovieDao.kinopoisk_id],
            set_={
                key: getattr(insert(MovieDao).excluded, key)
                for key in values
                if key != "kinopoisk_id"
            },
        )

        session.execute(stmt)

        result = session.execute(
            select(MovieDao).where(MovieDao.kinopoisk_id == values["kinopoisk_id"])
        ).scalar_one_or_none()

        return result
