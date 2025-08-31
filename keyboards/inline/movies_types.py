from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from api.kinopoisk.dto.movie import MovieType
from states.core.data_keys import MOVIE_TYPE
from utils.callbacks import callback_gen, Action


def movie_type_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
            text=movie_type.label,
            callback_data=callback_gen(
                None,
                Action.SELECT_MOVIE_TYPE,
                {MOVIE_TYPE: movie_type.value},
            ),
        )
        for movie_type in MovieType
    ]
    keyboard.add(*buttons)

    return keyboard
