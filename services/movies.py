from __future__ import annotations

from datetime import datetime, timedelta, timezone

from telebot.types import CallbackQuery

from api.kinopoisk.dto.core import KinopoiskSlug, SortType, SortField
from api.kinopoisk.dto.movie import MovieDto
from api.kinopoisk.dto.response import ResponseMovieSearch
from api.kinopoisk.kinopoisk_api import kinopoisk_api
from database.core.session import SessionLocal
from database.dao.users_movies_search_log import UserMovieSearchLog
from database.repos.movies import MovieRepository
from services.users import UserService


class MovieService:

    def __init__(
            self,
            genres_ttl: timedelta = timedelta(days=1),
    ) -> None:
        self._genres_ttl = genres_ttl
        self._genres_cache: list[KinopoiskSlug] | None = None
        self._genres_cached_at: datetime | None = None

    def get_genres(self):
        if self._is_genres_cache_valid():
            return self._genres_cache or []

        self._genres_cache = kinopoisk_api.get_genres()
        self._genres_cached_at = self._now()

        return self._genres_cache

    @classmethod
    def search_by_name(
            cls,
            user_id: int,
            search_name: str,
            page: int,
            page_size: int,
    ) -> ResponseMovieSearch:
        response = kinopoisk_api.search_movies_by_name(
            search_name=search_name,
            page=page,
            limit=page_size,
        )

        cls._log_user_movie_search(user_id, response.movies)

        return response

    @classmethod
    def search_by_rating(
            cls,
            page: int,
            page_size: int,
            rating_range: str,
            movie_type: str | None = None,
            genre: str | None = None,
    ) -> ResponseMovieSearch:
        return kinopoisk_api.search_movies(
            page=page,
            limit=page_size,
            movie_types=[movie_type] if movie_type else None,
            genres=[genre] if genre else None,
            rating_kp=[rating_range],
            sort_fields=[SortField.RATING_KINOPOISK, SortField.RATING_IMDB],
            sort_types=[SortType.DESC, SortType.DESC],
        )

    @classmethod
    def search_low_budget(
            cls,
            page: int,
            page_size: int,
            movie_type: str | None = None,
            genre: str | None = None,
    ) -> ResponseMovieSearch:
        return kinopoisk_api.search_movies(
            page=page,
            limit=page_size,
            movie_types=[movie_type] if movie_type else None,
            genres=[genre] if genre else None,
            sort_fields=[
                SortField.BUDGET,
                SortField.RATING_KINOPOISK, SortField.RATING_IMDB,
            ],
            sort_types=[
                SortType.ASC,
                SortType.DESC, SortType.DESC,
            ],
            not_null_fields=["budget.value"],
        )

    @classmethod
    def search_high_budget(
            cls,
            page: int,
            page_size: int,
            movie_type: str | None = None,
            genre: str | None = None,
    ) -> ResponseMovieSearch:
        return kinopoisk_api.search_movies(
            page=page,
            limit=page_size,
            movie_types=[movie_type] if movie_type else None,
            genres=[genre] if genre else None,
            sort_fields=[SortField.BUDGET_CURRENCY, SortField.BUDGET],
            sort_types=[SortType.ASC, SortType.DESC],
            not_null_fields=["budget.value", "budget.currency"],
        )

    def show_history(self, call: CallbackQuery) -> None:
        pass

    def _is_genres_cache_valid(self) -> bool:
        if not self._genres_cache or not self._genres_cached_at:
            return False

        return (self._now() - self._genres_cached_at) <= self._genres_ttl

    @classmethod
    def _log_user_movie_search(
            cls,
            user_tg_id: int,
            movies: list[MovieDto],
    ):
        with SessionLocal() as session:
            user = UserService.get_by_tg_id(user_tg_id)

            session.add_all(
                UserMovieSearchLog(
                    user_id=user.id,
                    movie_id=dao.id,
                )
                for dto in movies
                if (dao := MovieRepository.upsert_movie(session, dto))
            )

            session.commit()

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)


movie_service = MovieService()
