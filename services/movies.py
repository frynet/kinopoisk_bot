from telebot.types import CallbackQuery

from api.kinopoisk.dto.core import SortField, SortType
from api.kinopoisk.dto.response import ResponseMovieSearch
from api.kinopoisk.kinopoisk_api import kinopoisk_api


class MovieService:

    def get_genres(self):
        return kinopoisk_api.get_genres()

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

    def search_low_budget(self, call: CallbackQuery) -> None:
        pass

    def search_high_budget(self, call: CallbackQuery) -> None:
        pass

    def show_history(self, call: CallbackQuery) -> None:
        pass


movie_service = MovieService()
