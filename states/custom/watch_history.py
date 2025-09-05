from __future__ import annotations

from typing import Callable

from telebot.states import StatesGroup, State
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from errors.handlers import user_friendly_errors
from keyboards.inline.pagination import page_size_kb
from keyboards.inline.watch_history import history_period_kb
from loader import bot
from model.enums import HistoryPeriod
from services.movies import movie_service
from texts import USER_REQUEST_HISTORY_PERIOD, USER_REQUEST_PAGE_SIZE
from ..core import registry
from ..core.callbacks import SHOW_HISTORY_SET_PERIOD
from ..core.data_keys import UID, DATA_GETTER_FUNC, HISTORY_PERIOD
from ..core.registry import register
from ..default.pagination import PaginationStates

__all__ = [
    "watch_history",
    "watch_history_from_menu",
]


class WatchHistoryFlow(StatesGroup):
    period = State()


@user_friendly_errors
def watch_history_from_menu(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    watch_history(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        msg_id=call.message.message_id,
    )


def watch_history(
        user_id: int,
        chat_id: int,
        msg_id: int,
):
    state_data = {
        UID: user_id,
    }

    bot.delete_message(chat_id, msg_id)
    bot.set_state(user_id, WatchHistoryFlow.period, chat_id)
    bot.add_data(user_id, chat_id, **state_data)
    bot.send_message(chat_id, USER_REQUEST_HISTORY_PERIOD, reply_markup=history_period_kb())


@bot.callback_query_handler(cb_filter=SHOW_HISTORY_SET_PERIOD.filter())
@user_friendly_errors
def select_period(
        call: CallbackQuery,
        state: StateContext,
):
    chat_id = call.message.chat.id
    data = SHOW_HISTORY_SET_PERIOD.parse(call.data)

    with state.data() as ctx:
        ctx[HISTORY_PERIOD] = data[HISTORY_PERIOD]
        ctx[DATA_GETTER_FUNC] = registry.get_name(WatchHistoryFlow, "get_history")

    state.set(PaginationStates.set_page_size)

    bot.send_message(
        chat_id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=page_size_kb(),
    )


@register(WatchHistoryFlow, "get_history")
def _get_data(state: StateContext) -> Callable:
    with state.data() as ctx:
        uid = ctx.get(UID)
        period = HistoryPeriod.from_str(ctx[HISTORY_PERIOD])

    return lambda page, page_size: movie_service.get_user_search_history(
        user_id=uid,
        page=page, page_size=page_size,
        period=period,
    )
