from __future__ import annotations

from typing import Callable

from telebot.handler_backends import StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from errors.handlers import user_friendly_errors
from keyboards.inline.movies_types import movie_type_kb
from keyboards.inline.pagination import page_size_kb
from loader import bot
from services.movies import movie_service
from texts import (
    USER_REQUEST_PAGE_SIZE,
    USER_REQUEST_MOVIE_TYPE,
)
from ..core import registry
from ..core.data_keys import (
    MOVIE_TYPE, MOVIE_GENRE,
    NEXT_STEP_FUNC, DATA_GETTER_FUNC,
)
from ..core.registry import register
from ..default.pagination import PaginationStates
from ..default.search_movies import SearchMoviesStates

__all__ = ["start_search_high_budget"]


class SearchHighBudgetFlow(StatesGroup):
    pass


@user_friendly_errors
def start_search_high_budget(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    state_data = {
        NEXT_STEP_FUNC: registry.get_name(SearchHighBudgetFlow, "ask_pagination"),
        DATA_GETTER_FUNC: registry.get_name(SearchHighBudgetFlow, "search_high_budget"),
    }

    bot.delete_message(chat_id, msg_id)
    bot.set_state(user_id, SearchMoviesStates.select_type, chat_id)
    bot.add_data(user_id, chat_id, **state_data)
    bot.send_message(chat_id, USER_REQUEST_MOVIE_TYPE, reply_markup=movie_type_kb())


@register(SearchHighBudgetFlow, "ask_pagination")
def ask_pagination(chat_id: int, state: StateContext):
    state.set(PaginationStates.set_page_size)

    bot.send_message(chat_id, USER_REQUEST_PAGE_SIZE, reply_markup=page_size_kb())


@register(SearchHighBudgetFlow, "search_high_budget")
def _api_call(state: StateContext) -> Callable:
    with state.data() as ctx:
        movie_type = ctx.get(MOVIE_TYPE)
        genre = ctx.get(MOVIE_GENRE)

    return lambda page, page_size: movie_service.search_high_budget(
        page, page_size,
        movie_type=movie_type,
        genre=genre,
    )
