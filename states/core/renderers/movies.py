from typing import Callable

from telebot.states import State
from telebot.states.sync import StateContext
from telebot.types import Message

from api.kinopoisk.dto.movie import MovieDto
from api.kinopoisk.dto.response import ResponseMovieSearch
from keyboards.inline.movies import movie_actions_kb
from keyboards.inline.pagination import pagination_kb_text, pagination_kb
from loader import bot
from texts import BOT_SEARCH_RESULTS_NOT_FOUND
from utils.logging import log
from ..data_keys import CUR_PAGE, PAGE_SIZE, MAX_PAGES, OLD_MOVIES_IDS

__all__ = ["render_movies_page"]


def render_movies_page(
        chat_id: int,
        state: StateContext,
        reset_to_state: State,
        get_movies: Callable[[int, int], ResponseMovieSearch],
):
    state_data = {}

    with state.data() as ctx:
        page = ctx.get(CUR_PAGE, 1)
        page_size = ctx.get(PAGE_SIZE)

    resp = get_movies(page, page_size)

    if not resp.movies:
        bot.send_message(chat_id, BOT_SEARCH_RESULTS_NOT_FOUND)

        state.delete()
        state.set(reset_to_state)

        return

    state_data[MAX_PAGES] = resp.pages

    new_ids = []
    for movie in resp.movies:
        sent = send_movie(chat_id, movie)

        if sent:
            new_ids.append(sent.message_id)

    nav_msg = bot.send_message(
        chat_id,
        text=pagination_kb_text(resp.page, resp.pages),
        reply_markup=pagination_kb(),
    )

    state_data[OLD_MOVIES_IDS] = new_ids + [nav_msg.message_id]

    state.add_data(**state_data)


def send_movie(
        chat_id: int,
        movie: MovieDto,
) -> Message | None:
    """Отправляет карточку фильма"""

    text = str(movie)
    keyboard = movie_actions_kb(movie.id)

    try:
        if movie.poster and movie.poster.url:
            return bot.send_photo(
                chat_id,
                photo=str(movie.poster.url),
                caption=text,
                reply_markup=keyboard,
            )
        else:
            return bot.send_message(chat_id, text, reply_markup=keyboard)
    except Exception as e:
        log.error(f"Ошибка при отправке фильма: {e}")

    return None
