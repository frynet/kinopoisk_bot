from telebot.states import StatesGroup, State
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from keyboards.inline.movies_genres import genres_kb
from loader import bot
from services.movies import movie_service
from texts import USER_REQUEST_GENRE
from ..core.callbacks import MOVIE_SET_TYPE, MOVIE_NAV_GENRE, MOVIE_SET_GENRE
from ..core.data_keys import MOVIE_TYPE, MOVIE_GENRE, NEXT_STEP_FUNC, PREV_MSG_ID, PAGE
from ..core.registry import run


class SearchMoviesStates(StatesGroup):
    select_type = State()
    select_genre = State()


@bot.callback_query_handler(cb_filter=MOVIE_SET_TYPE.filter())
def select_movie_type(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    data = MOVIE_SET_TYPE.parse(call.data)
    movie_type = data.get(MOVIE_TYPE)

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


@bot.callback_query_handler(cb_filter=MOVIE_NAV_GENRE.filter(action="genre_nav"))
def genre_navigate(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    data = MOVIE_NAV_GENRE.parse(call.data)
    page = int(data.get(PAGE, 0))

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=genres_kb(
            genres=movie_service.get_genres(),
            page=page,
        ),
    )


@bot.callback_query_handler(cb_filter=MOVIE_SET_GENRE.filter())
def genre_select(
        call: CallbackQuery,
        state: StateContext,
):
    bot.answer_callback_query(call.id)

    data = MOVIE_SET_GENRE.parse(call.data)
    genre = data.get(MOVIE_GENRE)

    if not genre:
        return

    with state.data() as ctx:
        ctx[MOVIE_GENRE] = genre
        ctx[PREV_MSG_ID] = call.message.message_id
        next_step = ctx.get(NEXT_STEP_FUNC)

    if next_step:
        run(next_step, call.message.chat.id, state)
