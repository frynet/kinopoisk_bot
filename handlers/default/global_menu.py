from telebot.types import Message

from keyboards.reply.global_menu import BUTTON_MAIN_MENU, BUTTON_HELP
from loader import bot
from .help import bot_help
from .start import bot_start


@bot.message_handler(func=lambda m: m.text == BUTTON_MAIN_MENU)
def to_main_menu(msg: Message) -> None:
    bot_start(msg)


@bot.message_handler(func=lambda m: m.text == BUTTON_HELP)
def to_help(msg: Message) -> None:
    bot_help(msg)
