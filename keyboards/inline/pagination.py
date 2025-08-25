from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.default.pagination import PaginationStates
from texts import BTN_BACK_TXT, BTN_FORWARD_TXT
from utils.callbacks import callback_gen, Action


def build_pagination_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton(BTN_BACK_TXT, callback_data=callback_gen(PaginationStates, Action.PREV_PAGE)),
        InlineKeyboardButton(BTN_FORWARD_TXT, callback_data=callback_gen(PaginationStates, Action.NEXT_PAGE)),
    )

    return keyboard


def build_pagination_kb_text(
        page: int,
        max_pages: int,
) -> str:
    return f"📄 Страница {page} из {max_pages}"
