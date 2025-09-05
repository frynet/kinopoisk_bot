from itertools import zip_longest
from pathlib import Path
from typing import Callable

from telebot.apihelper import ApiTelegramException
from telebot.states.sync import StateContext
from telebot.types import InputMediaPhoto, InputFile

from api.kinopoisk.dto.movie import MovieDto
from assets.assets import MOVIE_PLACEHOLDER_PATH
from loader import bot
from model.movies import Movies
from texts import (
    BOT_SEARCH_RESULTS,
    BOT_SEARCH_RESULTS_NOT_FOUND,
)
from utils.logging import log
from ..data_keys import PAGE, PAGE_SIZE, MAX_PAGES, MOVIE_PAGE_IDS
from ...default.navigation import create_navigation

__all__ = ["render_movies_page"]


def render_movies_page(
        chat_id: int,
        state: StateContext,
        get_movies: Callable[[int, int], Movies],
):
    with state.data() as ctx:
        page = ctx.get(PAGE, 1)
        page_size = ctx.get(PAGE_SIZE)

        old_ids = ctx.get(MOVIE_PAGE_IDS)
        old_movie_ids, nav_msg_id = (old_ids[:-1], old_ids[-1]) if old_ids else ([], None)

    if not old_ids:
        bot.send_message(chat_id, BOT_SEARCH_RESULTS)

    movies = get_movies(page, page_size)

    if not movies.items:
        bot.send_message(chat_id, BOT_SEARCH_RESULTS_NOT_FOUND)
        state.delete()

        return

    new_movie_ids = []
    for movie, old_id in zip_longest(movies.items, old_movie_ids):
        if movie is not None:
            if sent := update_movie(chat_id, movie, old_id):
                new_movie_ids.append(sent)
        elif old_id:
            bot.delete_message(chat_id, old_id)

    nav_msg_id = create_navigation(movies.page, movies.pages, chat_id, nav_msg_id)

    state.add_data(
        **{
            MAX_PAGES: movies.pages,
            MOVIE_PAGE_IDS: [*new_movie_ids, nav_msg_id],
        }
    )


def update_movie(
        chat_id: int,
        movie: MovieDto,
        msg_id: int | None = None,
) -> int | None:
    """Отправляет карточку фильма или редактирует существующую."""

    txt = str(movie)

    if movie.poster and movie.poster.url:
        movie_img = str(movie.poster.url)
    else:
        movie_img = InputFile(Path(MOVIE_PLACEHOLDER_PATH).resolve())

    try:
        if msg_id:
            bot.edit_message_media(
                media=InputMediaPhoto(
                    media=movie_img,
                    caption=txt,
                    parse_mode="HTML",
                ),
                chat_id=chat_id,
                message_id=msg_id,
            )

            return msg_id
        else:
            msg = bot.send_photo(
                chat_id,
                photo=movie_img,
                caption=txt,
            )

            return msg.message_id
    except ApiTelegramException as e:
        log.error(f"Ошибка при обновлении фильма (msg_id={msg_id}): {e}")

    return None
