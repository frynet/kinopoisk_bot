from __future__ import annotations

from typing import Callable

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
from ..core import registry
from ..core.data_keys import (
    UID,
    MOVIE_TYPE, MOVIE_GENRE,
    NEXT_STEP_FUNC, DATA_GETTER_FUNC,
)
from ..core.registry import register
from ..default.pagination import PaginationStates
from ..default.search_movies import SearchMoviesStates

__all__ = [
    "search_low_budget",
    "search_low_budget_from_menu",
]


class SearchLowBudgetFlow(StatesGroup):
    pass


def search_low_budget_from_menu(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    search_low_budget(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        msg_id=call.message.message_id,
    )


def search_low_budget(
        user_id: int,
        chat_id: int,
        msg_id: int,
):
    state_data = {
        UID: user_id,
        NEXT_STEP_FUNC: registry.get_name(SearchLowBudgetFlow, "ask_pagination"),
        DATA_GETTER_FUNC: registry.get_name(SearchLowBudgetFlow, "search_low_budget"),
    }

    bot.delete_message(chat_id, msg_id)
    bot.set_state(user_id, SearchMoviesStates.select_type, chat_id)
    bot.add_data(user_id, chat_id, **state_data)
    bot.send_message(chat_id, USER_REQUEST_MOVIE_TYPE, reply_markup=movie_type_kb())


@register(SearchLowBudgetFlow, "ask_pagination")
def ask_pagination(chat_id: int, state: StateContext):
    state.set(PaginationStates.set_page_size)

    bot.send_message(chat_id, USER_REQUEST_PAGE_SIZE, reply_markup=page_size_kb())


@register(SearchLowBudgetFlow, "search_low_budget")
def _api_call(state: StateContext) -> Callable:
    with state.data() as ctx:
        uid = ctx.get(UID)
        movie_type = ctx.get(MOVIE_TYPE)
        genre = ctx.get(MOVIE_GENRE)

    return lambda page, page_size: movie_service.search_low_budget(
        user_id=uid,
        page=page, page_size=page_size,
        movie_type=movie_type,
        genre=genre,
    )
