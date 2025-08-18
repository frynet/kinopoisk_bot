from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BUTTON_HELP: str = "Помощь"
BUTTON_MAIN_MENU: str = "Главное меню"


def create_global_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_help = KeyboardButton(BUTTON_HELP)
    btn_main = KeyboardButton(BUTTON_MAIN_MENU)

    keyboard.add(btn_main, btn_help)

    return keyboard
