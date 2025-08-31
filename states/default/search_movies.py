from telebot.states import StatesGroup, State
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from keyboards.inline.movies_genres import genres_kb
from loader import bot
from services.movies import movie_service
from states.core.data_keys import MOVIE_TYPE, MOVIE_GENRE, NEXT_HANDLER_AFTER_GENRE, PREV_MSG_ID
from states.core.handlers.registry import execute_handler
from texts import USER_REQUEST_GENRE
from utils.callbacks import callback_match, Action, callback_parse


class SearchMoviesStates(StatesGroup):
    select_type = State()
    select_genre = State()


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

    state.set(SearchMoviesStates.select_genre)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=USER_REQUEST_GENRE,
        reply_markup=genres_kb(movie_service.get_genres()),
    )


@bot.callback_query_handler(
    func=callback_match(None, [Action.NAVIGATE_GENRES])
)
def genre_navigate(call: CallbackQuery):
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
def genre_select(
        call: CallbackQuery,
        state: StateContext,
):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    genre = data.payload.get(MOVIE_GENRE)

    if not genre:
        return

    with state.data() as ctx:
        ctx[MOVIE_GENRE] = genre
        ctx[PREV_MSG_ID] = call.message.message_id
        next_handler = ctx.get(NEXT_HANDLER_AFTER_GENRE)

    if next_handler:
        execute_handler(next_handler, call.message.chat.id, state)
