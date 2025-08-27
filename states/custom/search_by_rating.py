from __future__ import annotations

from telebot.handler_backends import State, StatesGroup
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from keyboards.inline.movie_genres import genres_kb
from keyboards.inline.pagination import page_size_kb
from keyboards.inline.search_by_rating import movie_type_kb, movie_rating_kb
from loader import bot
from services.movies import movie_service
from texts import (
    USER_REQUEST_PAGE_SIZE, USER_REQUEST_MOVIE_TYPE,
    USER_REQUEST_GENRE, USER_REQUEST_RATING_RANGE,
)
from utils.callbacks import callback_match, Action, callback_parse
from utils.telegram import delete_message
from ..core.data_keys import MOVIE_TYPE, MOVIE_RATING, MOVIE_GENRE
from ..core.handlers.movies import set_handlers, register_show_movies_handlers
from ..core.renderers.movies import render_movies_page
from ..default.pagination import PaginationStates

__all__ = ["search_by_rating_flow"]


class SearchByRatingFlow(StatesGroup):
    select_type = State()
    select_genre = State()
    select_rating = State()


def search_by_rating_flow(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    delete_message(bot, call.message)

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    bot.set_state(user_id, SearchByRatingFlow.select_type, chat_id)
    bot.send_message(
        chat_id,
        USER_REQUEST_MOVIE_TYPE,
        reply_markup=movie_type_kb(),
    )


@bot.callback_query_handler(
    func=callback_match(None, [Action.SELECT_MOVIE_TYPE])
)
def select_movie_type(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    movie_type = data.payload.get(MOVIE_TYPE)

    if not movie_type:
        return

    with state.data() as ctx:
        ctx[MOVIE_TYPE] = movie_type

    state.set(SearchByRatingFlow.select_genre)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=USER_REQUEST_GENRE,
        reply_markup=genres_kb(movie_service.get_genres()),
    )


@bot.callback_query_handler(
    func=callback_match(None, [Action.NAVIGATE_GENRES])
)
def genre_navigation(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    page = int(data.payload.get("page", 0))

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=genres_kb(
            genres=movie_service.get_genres(),
            page=page,
        ),
    )


@bot.callback_query_handler(
    func=callback_match(None, [Action.SELECT_GENRE])
)
def select_genre(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    genre = data.payload.get(MOVIE_GENRE)

    if not genre:
        return

    with state.data() as ctx:
        ctx[MOVIE_GENRE] = genre

    state.set(SearchByRatingFlow.select_rating)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
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
        reset_to_state=SearchByRatingFlow.select_type,
        get_movies=api_call,
    )


register_show_movies_handlers(SearchByRatingFlow, _show_movies)
