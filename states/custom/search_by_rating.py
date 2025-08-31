from __future__ import annotations

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

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
from utils.callbacks import callback_match, Action, callback_parse
from utils.telegram import delete_message
from ..core.data_keys import (
    MOVIE_TYPE, MOVIE_RATING, MOVIE_GENRE,
    NEXT_HANDLER_AFTER_GENRE, PREV_MSG_ID,
)
from ..core.handlers.movies import set_handlers, register_show_movies_handlers
from ..core.handlers.registry import get_key, register_handler
from ..core.renderers.movies import render_movies_page
from ..default.pagination import PaginationStates

__all__ = ["search_by_rating_flow"]

from ..default.search_movies import SearchMoviesStates


class SearchByRatingFlow(StatesGroup):
    select_rating = State()


def search_by_rating_flow(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    delete_message(bot, call.message)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    state_data = {
        NEXT_HANDLER_AFTER_GENRE: get_key(SearchByRatingFlow, "ask_for_rating")
    }

    bot.set_state(user_id, SearchMoviesStates.select_type, chat_id)
    bot.add_data(user_id, chat_id, **state_data)

    bot.send_message(
        chat_id,
        USER_REQUEST_MOVIE_TYPE,
        reply_markup=movie_type_kb(),
    )


@register_handler(SearchByRatingFlow, "ask_for_rating")
def ask_for_rating(chat_id: int, state: StateContext):
    with state.data() as ctx:
        prev_msg_id = ctx.get(PREV_MSG_ID)

    state.set(SearchByRatingFlow.select_rating)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=prev_msg_id,
        text=USER_REQUEST_RATING_RANGE,
        reply_markup=movie_rating_kb(SearchByRatingFlow),
    )


@bot.callback_query_handler(
    func=callback_match(SearchByRatingFlow, [Action.SELECT_RATING_RANGE])
)
def select_rating(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    rating = data.payload.get(MOVIE_RATING)

    if not rating:
        return

    with state.data() as ctx:
        ctx[MOVIE_RATING] = rating
        set_handlers(SearchByRatingFlow, ctx)

    state.set(PaginationStates.set_page_size)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=USER_REQUEST_PAGE_SIZE,
        reply_markup=page_size_kb(),
    )


def _show_movies(chat_id: int, state: StateContext):
    with state.data() as ctx:
        movie_type = ctx.get(MOVIE_TYPE)
        genre = ctx.get(MOVIE_GENRE)
        rating_range = ctx.get(MOVIE_RATING)

    api_call = lambda page, page_size: movie_service.search_by_rating(
        movie_type=movie_type,
        genre=genre,
        rating_range=rating_range,
        page=page,
        page_size=page_size,
    )

    render_movies_page(
        chat_id=chat_id,
        state=state,
        reset_to_state=SearchMoviesStates.select_type,
        get_movies=api_call,
    )


register_show_movies_handlers(SearchByRatingFlow, _show_movies)
