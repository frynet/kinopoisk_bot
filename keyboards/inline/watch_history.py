from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from model.enums import HistoryPeriod
from states.core.callbacks import SHOW_HISTORY_SET_PERIOD
from states.core.data_keys import HISTORY_PERIOD


def history_period_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
            period.value, callback_data=SHOW_HISTORY_SET_PERIOD.new(**{HISTORY_PERIOD: period.name})
        )
        for period in HistoryPeriod
    ]

    keyboard.add(*buttons)

    return keyboard
