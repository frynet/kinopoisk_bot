from __future__ import annotations

from typing import Callable

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery, Message

from errors.app import AppError
from errors.handlers import user_friendly_errors
from keyboards.inline.pagination import page_size_kb
from loader import bot
from services.movies import movie_service
from texts import (
    ERR_GIVEN_EMPTY_NAME,
    USER_REQUEST_MOVIE_NAME, USER_REQUEST_PAGE_SIZE,
)
from ..core import registry
from ..core.data_keys import MOVIE_NAME, DATA_GETTER_FUNC
from ..core.registry import register
from ..default.pagination import PaginationStates

__all__ = ["start_search_by_name"]


class SearchByNameFlow(StatesGroup):
    name = State()


@user_friendly_errors
def start_search_by_name(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    bot.delete_message(chat_id, msg_id)
    bot.set_state(user_id, SearchByNameFlow.name, chat_id)
    bot.send_message(chat_id, USER_REQUEST_MOVIE_NAME)


@bot.message_handler(state=SearchByNameFlow.name)
@user_friendly_errors
def get_name(msg: Message, state: StateContext):
    name = (msg.text or "").strip()

    if not name:
        raise AppError(ERR_GIVEN_EMPTY_NAME)

    with state.data() as ctx:
        ctx[MOVIE_NAME] = name
        ctx[DATA_GETTER_FUNC] = registry.get_name(SearchByNameFlow, "search_by_name")

    state.set(PaginationStates.set_page_size)

    bot.send_message(
        msg.chat.id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=page_size_kb(),
    )


@register(SearchByNameFlow, "search_by_name")
def _api_call(state: StateContext) -> Callable:
    with state.data() as ctx:
        name = ctx.get(MOVIE_NAME)

    return lambda page, page_size: movie_service.search_by_name(name, page, page_size)
