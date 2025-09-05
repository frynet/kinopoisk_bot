from __future__ import annotations

from math import ceil

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton as Btn

from api.kinopoisk.dto.core import KinopoiskSlug
from states.core.callbacks import MOVIE_SET_GENRE, MOVIE_NAV_GENRE
from states.core.data_keys import MOVIE_GENRE, CB_ACTION, PAGE
from texts import BTN_BACK_TXT, BTN_FORWARD_TXT

GENRES_PER_PAGE = 8


def genres_kb(
        genres: list[KinopoiskSlug],
        page: int = 0,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    max_pages = ceil(len(genres) / GENRES_PER_PAGE)
    page = max(0, min(page, max(max_pages - 1, 0)))

    start = page * GENRES_PER_PAGE
    end = start + GENRES_PER_PAGE

    buttons = [
        Btn(
            text=genre.name.capitalize(),
            callback_data=MOVIE_SET_GENRE.new(**{MOVIE_GENRE: genre.name}),
        )
        for genre in genres[start:end]
    ]
    if buttons:
        keyboard.add(*buttons)

    nav = []
    if page > 0:
        nav.append(
            Btn(
                text=BTN_BACK_TXT,
                callback_data=MOVIE_NAV_GENRE.new(
                    **{
                        CB_ACTION: "genre_nav",
                        PAGE: str(page - 1),
                    }
                )
            )
        )
    if page + 1 < max_pages:
        nav.append(
            Btn(
                text=BTN_FORWARD_TXT,
                callback_data=MOVIE_NAV_GENRE.new(
                    **{
                        CB_ACTION: "genre_nav",
                        PAGE: str(page + 1),
                    }
                )
            )
        )
    if nav:
        keyboard.row(*nav)

    return keyboard
