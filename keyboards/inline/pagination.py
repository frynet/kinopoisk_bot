from typing import Iterable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.core.data_keys import PAGE_SIZE
from texts import BTN_BACK_TXT, BTN_FORWARD_TXT
from utils.callbacks import callback_gen, Action


def page_size_kb(options: Iterable[int] = (1, 3, 5)) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    row = [
        InlineKeyboardButton(
            text=str(opt),
            callback_data=callback_gen(
                None,
                Action.SET_PAGE_SIZE,
                {PAGE_SIZE: str(opt)}
            ),
        )
        for opt in options
    ]

    keyboard.row(*row)

    return keyboard


def pagination_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(BTN_BACK_TXT, callback_data=callback_gen(None, Action.PREV_PAGE)),
        InlineKeyboardButton(BTN_FORWARD_TXT, callback_data=callback_gen(None, Action.NEXT_PAGE)),
    )

    return keyboard


def pagination_kb_text(
        page: int,
        max_pages: int,
) -> str:
    return f"📄 Страница {page} из {max_pages}"
