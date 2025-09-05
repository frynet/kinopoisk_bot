from telebot.types import Message

from errors.handlers import user_friendly_errors
from loader import bot
from states.custom.search_low_budget import search_low_budget


@bot.message_handler(commands=["low_budget_movie"])
@user_friendly_errors
def bot_help(msg: Message):
    search_low_budget(
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        msg_id=msg.message_id,
    )
