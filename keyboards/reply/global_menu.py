from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from texts import BTN_HELP_TXT, BTN_MAIN_MENU_TXT


def create_global_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_help = KeyboardButton(BTN_HELP_TXT)
    btn_main = KeyboardButton(BTN_MAIN_MENU_TXT)

    keyboard.add(btn_main, btn_help)

    return keyboard
