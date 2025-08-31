from __future__ import annotations

from datetime import datetime, timedelta, timezone

from telebot.types import CallbackQuery

from api.kinopoisk.dto.core import KinopoiskSlug, SortType, SortField
from api.kinopoisk.dto.response import ResponseMovieSearch
from api.kinopoisk.kinopoisk_api import kinopoisk_api


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

    def search_by_name(
            self,
            search_name: str,
            page: int,
            page_size: int,
    ) -> ResponseMovieSearch:
        return kinopoisk_api.search_movies_by_name(
            search_name=search_name,
            page=page,
            limit=page_size,
        )

    def search_by_rating(
            self,
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

    def search_low_budget(
            self,
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
            sort_fields=[SortField.BUDGET],
            sort_types=[SortType.ASC],
            not_null_fields=["budget.value"],
        )

    def search_high_budget(
            self,
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
            sort_fields=[SortField.BUDGET],
            sort_types=[SortType.DESC],
        )

    def show_history(self, call: CallbackQuery) -> None:
        pass

    def _is_genres_cache_valid(self) -> bool:
        if not self._genres_cache or not self._genres_cached_at:
            return False

        return (self._now() - self._genres_cached_at) <= self._genres_ttl

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)


movie_service = MovieService()
