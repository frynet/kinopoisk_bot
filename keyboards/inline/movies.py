from __future__ import annotations

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.core.data_keys import MOVIE_ID
from texts import BTN_MOVIE_WATCHED, BTN_MOVIE_UNWATCHED
from utils.callbacks import callback_gen, Action


def movie_actions_kb(movie_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.row(
        InlineKeyboardButton(
            BTN_MOVIE_WATCHED,
            callback_data=callback_gen(
                None, Action.MARK_WATCHED,
                {MOVIE_ID: str(movie_id)},
            ),
        ),
        InlineKeyboardButton(
            BTN_MOVIE_UNWATCHED,
            callback_data=callback_gen(
                None, Action.MARK_UNWATCHED,
                {MOVIE_ID: str(movie_id)},
            ),
        ),
    )

    return keyboard
