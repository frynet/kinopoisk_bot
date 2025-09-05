from __future__ import annotations

from typing import Callable

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from errors.handlers import user_friendly_errors
from keyboards.inline.movies_types import movie_type_kb
from keyboards.inline.pagination import page_size_kb
from keyboards.inline.search_by_rating import movie_rating_kb
from loader import bot
from services.movies import movie_service
from texts import (
    USER_REQUEST_PAGE_SIZE,
    USER_REQUEST_MOVIE_TYPE,
    USER_REQUEST_RATING_RANGE,
)
from ..core import registry
from ..core.callbacks import RATING_FLOW_SET_RATE
from ..core.data_keys import (
    MOVIE_TYPE, MOVIE_RATING, MOVIE_GENRE,
    NEXT_STEP_FUNC, PREV_MSG_ID, DATA_GETTER_FUNC, UID,
)
from ..core.registry import register
from ..default.pagination import PaginationStates
from ..default.search_movies import SearchMoviesStates

__all__ = ["start_search_by_rating"]


class SearchByRatingFlow(StatesGroup):
    select_rating = State()


@user_friendly_errors
def start_search_by_rating(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    state_data = {
        UID: user_id,
        NEXT_STEP_FUNC: registry.get_name(SearchByRatingFlow, "ask_for_rating"),
        DATA_GETTER_FUNC: registry.get_name(SearchByRatingFlow, "search_by_rating"),
    }

    bot.delete_message(chat_id, msg_id)
    bot.set_state(user_id, SearchMoviesStates.select_type, chat_id)
    bot.add_data(user_id, chat_id, **state_data)
    bot.send_message(chat_id, USER_REQUEST_MOVIE_TYPE, reply_markup=movie_type_kb())


@register(SearchByRatingFlow, "ask_for_rating")
def ask_for_rating(chat_id: int, state: StateContext):
    with state.data() as ctx:
        prev_msg_id = ctx.get(PREV_MSG_ID)

    state.set(SearchByRatingFlow.select_rating)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=prev_msg_id,
        text=USER_REQUEST_RATING_RANGE,
        reply_markup=movie_rating_kb(),
    )


@bot.callback_query_handler(cb_filter=RATING_FLOW_SET_RATE.filter())
@user_friendly_errors
def select_rating(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = RATING_FLOW_SET_RATE.parse(call.data)
    rating = data.get(MOVIE_RATING)

    with state.data() as ctx:
        ctx[MOVIE_RATING] = rating

    state.set(PaginationStates.set_page_size)
    bot.edit_message_text(USER_REQUEST_PAGE_SIZE, chat_id, msg_id, reply_markup=page_size_kb())


@register(SearchByRatingFlow, "search_by_rating")
def _api_call(state: StateContext) -> Callable:
    with state.data() as ctx:
        uid = ctx.get(UID)
        movie_type = ctx.get(MOVIE_TYPE)
        genre = ctx.get(MOVIE_GENRE)
        rating_range = ctx.get(MOVIE_RATING)

    return lambda page, page_size: movie_service.search_by_rating(
        user_id=uid,
        movie_type=movie_type,
        genre=genre,
        rating_range=rating_range,
        page=page,
        page_size=page_size,
    )
