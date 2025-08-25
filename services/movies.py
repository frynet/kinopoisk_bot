from telebot.types import CallbackQuery

from api.kinopoisk.dto.response import ResponseMovieSearch
from api.kinopoisk.kinopoisk_api import kinopoisk_api


class MovieService:

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

    def search_by_rating(self, call: CallbackQuery) -> None:
        pass

    def search_low_budget(self, call: CallbackQuery) -> None:
        pass

    def search_high_budget(self, call: CallbackQuery) -> None:
        pass

    def show_history(self, call: CallbackQuery) -> None:
        pass


movie_service = MovieService()
