from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton as Btn

from api.kinopoisk.dto.movie import MovieType
from states.core.callbacks import MOVIE_SET_TYPE
from states.core.data_keys import MOVIE_TYPE


def movie_type_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        Btn(
            text=movie_type.label,
            callback_data=MOVIE_SET_TYPE.new(**{MOVIE_TYPE: movie_type.value}),
        )
        for movie_type in MovieType
    ]
    keyboard.add(*buttons)

    return keyboard
