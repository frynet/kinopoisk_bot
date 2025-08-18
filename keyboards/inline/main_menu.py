from dataclasses import dataclass
from enum import Enum
from typing import Callable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import bot
from services.movies import movie_service

__all__ = ["create_main_menu"]


@dataclass(frozen=True)
class MenuItem:
    text: str
    handler: Callable[[CallbackQuery], None]


class MainMenuButton(Enum):
    SEARCH_BY_NAME = MenuItem("🎬 Поиск по названию", movie_service.search_by_name)
    SEARCH_BY_RATING = MenuItem("⭐ Поиск по рейтингу", movie_service.search_by_rating)
    SEARCH_LOW_BUDGET = MenuItem("💸 С низким бюджетом", movie_service.search_low_budget)
    SEARCH_HIGH_BUDGET = MenuItem("💰 С высоким бюджетом", movie_service.search_high_budget)
    SEARCH_HISTORY = MenuItem("📜 История поиска", movie_service.show_history)


def create_main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    for btn in MainMenuButton:
        markup.add(InlineKeyboardButton(text=btn.value.text, callback_data=btn.name))

    return markup


@bot.callback_query_handler(func=lambda call: call.data in MainMenuButton.__members__)
def _main_menu_router(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    btn = MainMenuButton[call.data]
    btn.value.handler(call)
