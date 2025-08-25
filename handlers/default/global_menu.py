from telebot.types import Message

from loader import bot
from texts import BTN_HELP_TXT, BTN_MAIN_MENU_TXT
from .help import bot_help
from .start import bot_start


@bot.message_handler(func=lambda m: m.text == BTN_MAIN_MENU_TXT)
def to_main_menu(msg: Message) -> None:
    bot_start(msg)


@bot.message_handler(func=lambda m: m.text == BTN_HELP_TXT)
def to_help(msg: Message) -> None:
    bot_help(msg)
