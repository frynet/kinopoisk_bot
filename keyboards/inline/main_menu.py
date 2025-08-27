from dataclasses import dataclass
from enum import Enum
from typing import Callable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import bot
from services.movies import movie_service
from states.custom.search_by_name import search_by_name_flow
from states.custom.search_by_rating import start_search_by_rating_flow
from texts import (
    BTN_SEARCH_BY_NAME,
    BTN_SEARCH_BY_RATING,
    BTN_SEARCH_LOW_BUDGET,
    BTN_SEARCH_HIGH_BUDGET,
    BTN_SEARCH_HISTORY,
)

__all__ = ["create_main_menu"]


@dataclass(frozen=True)
class MenuItem:
    text: str
    handler: Callable[[CallbackQuery], None]


class MainMenuButton(Enum):
    SEARCH_BY_NAME = MenuItem(BTN_SEARCH_BY_NAME, search_by_name_flow)
    SEARCH_BY_RATING = MenuItem(BTN_SEARCH_BY_RATING, start_search_by_rating_flow)
    SEARCH_LOW_BUDGET = MenuItem(BTN_SEARCH_LOW_BUDGET, movie_service.search_low_budget)
    SEARCH_HIGH_BUDGET = MenuItem(BTN_SEARCH_HIGH_BUDGET, movie_service.search_high_budget)
    SEARCH_HISTORY = MenuItem(BTN_SEARCH_HISTORY, movie_service.show_history)


def create_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for btn in MainMenuButton:
        keyboard.add(InlineKeyboardButton(text=btn.value.text, callback_data=btn.name))

    return keyboard


@bot.callback_query_handler(func=lambda call: call.data in MainMenuButton.__members__)
def _main_menu_router(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    btn = MainMenuButton[call.data]
    btn.value.handler(call)
