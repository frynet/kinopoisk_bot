from telebot.types import Message

from errors.handlers import user_friendly_errors
from loader import bot
from states.custom.search_high_budget import search_high_budget


@bot.message_handler(commands=["high_budget_movie"])
@user_friendly_errors
def bot_help(msg: Message):
    search_high_budget(
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        msg_id=msg.message_id,
    )
