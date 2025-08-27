from typing import Callable

from telebot.states import StatesGroup
from telebot.states.sync import StateContext

from loader import bot
from texts import BOT_SEARCH_RESULTS
from utils.telegram import delete_message_by_id
from .registry import get_key, register_handler
from ..data_keys import INITIAL_HANDLER, UPDATE_HANDLER, OLD_MOVIES_IDS

SHOW_FIRST_PAGE = "init_page"
SHOW_OTHER_PAGE = "update_page"
RenderMoviesFunc = Callable[[int, StateContext], None]


def set_handlers(flow: type[StatesGroup], state_data: dict):
    state_data[INITIAL_HANDLER] = get_key(flow, SHOW_FIRST_PAGE)
    state_data[UPDATE_HANDLER] = get_key(flow, SHOW_OTHER_PAGE)


def register_show_movies_handlers(
        flow: type[StatesGroup],
        render_movies_func: RenderMoviesFunc,
):
    @register_handler(flow, SHOW_FIRST_PAGE)
    def init_page(chat_id: int, state: StateContext):
        """Первичное отображение результатов поиска."""
        bot.send_message(chat_id, BOT_SEARCH_RESULTS)
        render_movies_func(chat_id, state)

    @register_handler(flow, SHOW_OTHER_PAGE)
    def update_page(chat_id: int, state: StateContext):
        with state.data() as ctx:
            old_ids = ctx.get(OLD_MOVIES_IDS, [])

        for msg_id in old_ids:
            delete_message_by_id(bot, chat_id, msg_id)

        render_movies_func(chat_id, state)
