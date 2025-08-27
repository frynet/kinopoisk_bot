from __future__ import annotations

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery, Message

from keyboards.inline.pagination import page_size_kb
from loader import bot
from services.movies import movie_service
from texts import (
    ERR_GIVEN_EMPTY_NAME,
    USER_REQUEST_MOVIE_NAME, USER_REQUEST_PAGE_SIZE,
)
from ..core.data_keys import MOVIE_NAME
from ..core.handlers.movies import set_handlers, register_show_movies_handlers
from ..core.renderers.movies import render_movies_page
from ..default.pagination import PaginationStates

__all__ = ["start_search_by_name_flow"]


class SearchByNameFlow(StatesGroup):
    name = State()


def start_search_by_name_flow(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    bot.set_state(user_id, SearchByNameFlow.name, chat_id)
    bot.send_message(
        chat_id,
        USER_REQUEST_MOVIE_NAME,
    )


@bot.message_handler(state=SearchByNameFlow.name)
def handle_name_input(msg: Message, state: StateContext):
    name = (msg.text or "").strip()

    if not name:
        bot.reply_to(msg, ERR_GIVEN_EMPTY_NAME)
        return

    with state.data() as ctx:
        ctx[MOVIE_NAME] = name
        set_handlers(SearchByNameFlow, ctx)

    state.set(PaginationStates.set_page_size)

    bot.send_message(
        msg.chat.id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=page_size_kb(),
    )


def _render_movies(chat_id, state):
    with state.data() as ctx:
        name = ctx.get(MOVIE_NAME)

    api_call = lambda page, page_size: movie_service.search_by_name(name, page, page_size)

    render_movies_page(
        chat_id=chat_id,
        state=state,
        reset_to_state=SearchByNameFlow.name,
        get_movies=api_call,
    )


register_show_movies_handlers(SearchByNameFlow, _render_movies)
