from __future__ import annotations

from telebot.handler_backends import StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from keyboards.inline.movies_types import movie_type_kb
from keyboards.inline.pagination import page_size_kb
from loader import bot
from services.movies import movie_service
from texts import (
    USER_REQUEST_PAGE_SIZE,
    USER_REQUEST_MOVIE_TYPE,
)
from utils.telegram import delete_message
from ..core.data_keys import (
    MOVIE_TYPE, MOVIE_GENRE,
    NEXT_HANDLER_AFTER_GENRE,
)
from ..core.handlers.movies import set_handlers, register_show_movies_handlers
from ..core.handlers.registry import get_key, register_handler
from ..core.renderers.movies import render_movies_page
from ..default.pagination import PaginationStates

__all__ = ["search_high_budget_flow"]

from ..default.search_movies import SearchMoviesStates


class SearchHighBudgetFlow(StatesGroup):
    pass


def search_high_budget_flow(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    delete_message(bot, call.message)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    state_data = {
        NEXT_HANDLER_AFTER_GENRE: get_key(SearchHighBudgetFlow, "ask_pagination")
    }

    bot.set_state(user_id, SearchMoviesStates.select_type, chat_id)
    bot.add_data(user_id, chat_id, **state_data)

    bot.send_message(
        chat_id,
        USER_REQUEST_MOVIE_TYPE,
        reply_markup=movie_type_kb(),
    )


@register_handler(SearchHighBudgetFlow, "ask_pagination")
def ask_pagination(chat_id: int, state: StateContext):
    with state.data() as ctx:
        set_handlers(SearchHighBudgetFlow, ctx)

    state.set(PaginationStates.set_page_size)

    bot.send_message(
        chat_id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=page_size_kb(),
    )


def _show_movies(chat_id: int, state: StateContext):
    with state.data() as ctx:
        movie_type = ctx.get(MOVIE_TYPE)
        genre = ctx.get(MOVIE_GENRE)

    api_call = lambda page, page_size: movie_service.search_high_budget(
        page, page_size,
        movie_type=movie_type,
        genre=genre,
    )

    render_movies_page(chat_id, state, get_movies=api_call)


register_show_movies_handlers(SearchHighBudgetFlow, _show_movies)
