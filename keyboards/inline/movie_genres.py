from __future__ import annotations

from math import ceil

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from api.kinopoisk.dto.core import KinopoiskSlug
from states.core.data_keys import MOVIE_GENRE
from texts import BTN_BACK_TXT, BTN_FORWARD_TXT
from utils.callbacks import callback_gen, Action

GENRES_PER_PAGE = 8


def genres_kb(
        genres: list[KinopoiskSlug],
        page: int = 0,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    def btn(txt: str, act: Action, pay: dict[str, str]):
        return InlineKeyboardButton(txt, callback_data=callback_gen(None, act, pay))

    max_pages = ceil(len(genres) / GENRES_PER_PAGE)
    page = max(0, min(page, max(max_pages - 1, 0)))

    start = page * GENRES_PER_PAGE
    end = start + GENRES_PER_PAGE

    buttons = [
        btn(genre.name.capitalize(), Action.SELECT_GENRE, {MOVIE_GENRE: genre.slug})
        for genre in genres[start:end]
    ]
    if buttons:
        keyboard.add(*buttons)

    nav = []
    if page > 0:
        nav.append(btn(BTN_BACK_TXT, Action.NAVIGATE_GENRES, {"page": str(page - 1)}))
    if page + 1 < max_pages:
        nav.append(btn(BTN_FORWARD_TXT, Action.NAVIGATE_GENRES, {"page": str(page + 1)}))
    if nav:
        keyboard.row(*nav)

    return keyboard
