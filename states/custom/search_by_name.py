from __future__ import annotations

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery, Message

from keyboards.inline.search_by_name import build_page_size_inline_kb
from loader import bot
from services.movies import movie_service
from states.data_keys import (
    INITIAL_HANDLER, UPDATE_HANDLER,
    MOVIE_NAME, SENT_MOVIES_IDS,
)
from states.default.pagination import PaginationStates
from states.registry import register_handler, get_key
from states.renderers.movies import send_movies
from texts import (
    BOT_SEARCH_RESULTS, ERR_GIVEN_EMPTY_NAME,
    USER_REQUEST_MOVIE_NAME, USER_REQUEST_PAGE_SIZE,
)
from utils.telegram import delete_message_by_id

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
        ctx[INITIAL_HANDLER] = get_key(SearchByNameFlow, "show_initial_page")
        ctx[UPDATE_HANDLER] = get_key(SearchByNameFlow, "show_updated_page")

    state.set(PaginationStates.set_page_size)

    bot.send_message(
        msg.chat.id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=build_page_size_inline_kb(),
    )


@register_handler(SearchByNameFlow, "show_initial_page")
def show_initial_page(chat_id: int, state: StateContext):
    """Первичное отображение результатов поиска."""
    bot.send_message(chat_id, BOT_SEARCH_RESULTS)

    _show_movies_page(chat_id, state)


@register_handler(SearchByNameFlow, "show_updated_page")
def show_updated_page(chat_id: int, state: StateContext):
    with state.data() as ctx:
        old_ids = ctx.get(SENT_MOVIES_IDS, [])

    for msg_id in old_ids:
        delete_message_by_id(bot, chat_id, msg_id)

    _show_movies_page(chat_id, state)


def _show_movies_page(chat_id, state):
    with state.data() as ctx:
        name = ctx.get(MOVIE_NAME)

    api_call = lambda page, page_size: movie_service.search_by_name(name, page, page_size)

    send_movies(
        chat_id=chat_id,
        state=state,
        reset_to_state=SearchByNameFlow.name,
        get_movies=api_call,
    )
