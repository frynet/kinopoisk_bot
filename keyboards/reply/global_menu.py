from telebot.types import ReplyKeyboardMarkup

from keyboards.common import BTN_HELP, BTN_MAIN_MENU


def create_global_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(BTN_MAIN_MENU, BTN_HELP)

    return keyboard
