from telebot.callback_data import CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import CallbackQuery


class CallbackQueryFilter(AdvancedCustomFilter):
    key = 'cb_filter'

    def check(self, call: CallbackQuery, cb_filter: CallbackDataFilter) -> bool:
        return cb_filter.check(call)
