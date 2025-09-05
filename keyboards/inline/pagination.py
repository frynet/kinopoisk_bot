from typing import Iterable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton as Btn

from states.core.callbacks import PAGINATION_SET_SIZE, PAGINATION_NAV_PAGE
from states.core.data_keys import PAGE_SIZE
from texts import BTN_BACK_TXT, BTN_FORWARD_TXT


def page_size_kb(options: Iterable[int] = (1, 3, 5)) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    row = [
        Btn(
            text=str(opt),
            callback_data=PAGINATION_SET_SIZE.new(**{PAGE_SIZE: str(opt)}),
        )
        for opt in options
    ]

    keyboard.row(*row)

    return keyboard


def pagination_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        Btn(BTN_BACK_TXT, callback_data=PAGINATION_NAV_PAGE.new(action="prev")),
        Btn(BTN_FORWARD_TXT, callback_data=PAGINATION_NAV_PAGE.new(action="next")),
    )

    return keyboard


def pagination_kb_text(
        page: int,
        max_pages: int,
) -> str:
    return f"📄 Страница {page} из {max_pages}"
