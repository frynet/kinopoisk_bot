from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, List

from requests import Session

import config
from errors.api.kinopoisk import KinopoiskApiError
from utils.errors import log_request_error
from utils.logging import log
from utils.models import get_required_fields
from .dto.core import KinopoiskSlug, SortType, SortField
from .dto.movie import MovieDto
from .dto.response import ResponseMovieSearch

__all__ = ["kinopoisk_api"]

BASE_URL = "https://api.kinopoisk.dev"


class KinopoiskApi:

    def __init__(
            self,
            api_key: str,
            base_url: str,
            request_timeout: int = 10,
            genres_ttl: timedelta = timedelta(days=1),
    ) -> None:
        self._base_url = base_url
        self._timeout = request_timeout
        self._genres_ttl = genres_ttl

        self._session = Session()
        self._session.headers.update(
            {
                "X-API-KEY": api_key,
                "accept": "application/json",
            }
        )

        self._genres_cache: List[KinopoiskSlug] | None = None
        self._genres_cached_at: datetime | None = None

    def get_genres(self) -> List[KinopoiskSlug]:

        if self._is_genres_cache_valid():
            return self._genres_cache or []

        url = f"{self._base_url}/v1/movie/possible-values-by-field"
        params = {"field": "genres.name"}
        data = self._request("GET", url, params)

        if not isinstance(data, list):
            log.error(
                "Unexpected genres response format: expected list, got {}. Payload preview: {}",
                type(data).__name__,
                str(data)[:500],
            )

            raise KinopoiskApiError("Unexpected genres response format")

        genres = [
            KinopoiskSlug(
                name=it["name"].strip(),
                slug=it["slug"].strip(),
            )
            for it in data
            if isinstance(it, dict)
               and it.get("name")
               and it.get("slug")
        ]

        self._genres_cache = genres
        self._genres_cached_at = self._now()

        return genres

    def search_movies_by_name(
            self,
            search_name: str,
            page: int | None = None,
            limit: int | None = None,
    ) -> ResponseMovieSearch:

        url = f"{self._base_url}/v1.4/movie/search"
        params = {
            "query": search_name.strip(),
        }

        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)

        data = self._request("GET", url, params=params)

        return ResponseMovieSearch(**data)

    def search_movies(
            self,
            page: int = 1,
            limit: int = 10,
            *,
            movie_types: list[str] | None = None,
            genres: list[KinopoiskSlug] | None = None,
            rating_kp: list[str] | None = None,
            sort_fields: list[SortField] | None = None,
            sort_types: list[SortType] | None = None,
    ) -> ResponseMovieSearch:
        url = f"{self._base_url}/v1.4/movie"

        params: dict[str, Any] = {
            "page": page,
            "limit": limit,
            "selectFields": get_required_fields(MovieDto),
        }

        if sort_fields:
            params["sortField"] = [sf.value for sf in sort_fields]

        if sort_types:
            params["sortType"] = [st.value for st in sort_types]

        if movie_types:
            params["type"] = movie_types

        if rating_kp:
            params["rating.kp"] = [str(r) for r in rating_kp]

        if genres:
            params["genres.name"] = [
                f"+{genre.name}"
                for genre in genres
            ]

        data = self._request("GET", url, params=params)

        return ResponseMovieSearch(**data)

    @log_request_error(KinopoiskApiError)
    def _request(
            self,
            method: str,
            url: str,
            params: dict[str, Any] | None = None,
    ) -> Any:
        response = self._session.request(method, url, params=params, timeout=self._timeout)
        response.raise_for_status()

        return response.json()

    def _is_genres_cache_valid(self) -> bool:
        if not self._genres_cache or not self._genres_cached_at:
            return False

        return (self._now() - self._genres_cached_at) <= self._genres_ttl

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)


kinopoisk_api = KinopoiskApi(
    api_key=config.KINOPOISK_API_KEY,
    base_url=BASE_URL,
)
