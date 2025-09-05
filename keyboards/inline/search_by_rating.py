from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton as Btn

from states.core.callbacks import RATING_FLOW_SET_RATE
from states.core.data_keys import MOVIE_RATING

RATING_OPTIONS = {
    "🏆 Шедевры": "9-10",
    "👍 Отличные": "8-9",
    "👌 Хорошие": "7-8",
    "😐 Средние": "5-7",
    "🎲 Все": "1-10",
}


def movie_rating_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        Btn(
            text=label,
            callback_data=RATING_FLOW_SET_RATE.new(**{MOVIE_RATING: value}),
        )
        for label, value in RATING_OPTIONS.items()
    ]
    keyboard.add(*buttons)

    return keyboard
