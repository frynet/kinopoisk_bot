from telebot.types import BotCommand

from config import DEFAULT_COMMANDS


def set_default_commands(bot):
    bot.set_my_commands(
        [
            BotCommand(*cmd)
            for cmd in DEFAULT_COMMANDS
        ]
    )
