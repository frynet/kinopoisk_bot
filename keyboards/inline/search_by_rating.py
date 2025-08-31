from telebot.states import StatesGroup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.core.data_keys import MOVIE_RATING
from utils.callbacks import callback_gen, Action

RATING_OPTIONS = {
    "🏆 Шедевры": "9-10",
    "👍 Отличные": "8-9",
    "👌 Хорошие": "7-8",
    "😐 Средние": "5-7",
    "🎲 Все": "1-10",
}


def movie_rating_kb(flow: type[StatesGroup]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=callback_gen(
                flow,
                Action.SELECT_RATING_RANGE,
                {MOVIE_RATING: value},
            ),
        )
        for label, value in RATING_OPTIONS.items()
    ]
    keyboard.add(*buttons)

    return keyboard
