from __future__ import annotations

from collections.abc import Iterable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.data_keys import PAGE_SIZE, MOVIE_ID
from states.default.pagination import PaginationStates
from texts import BTN_MOVIE_WATCHED, BTN_MOVIE_UNWATCHED
from utils.callbacks import callback_gen, Action


def build_page_size_inline_kb(options: Iterable[int] = (1, 3, 5)) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    row = [
        InlineKeyboardButton(
            text=str(opt),
            callback_data=callback_gen(
                PaginationStates,
                Action.SET_PAGE_SIZE,
                {PAGE_SIZE: str(opt)}
            ),
        )
        for opt in options
    ]

    keyboard.row(*row)

    return keyboard


def build_movie_actions_inline_kb(movie_id: int) -> InlineKeyboardMarkup:
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
