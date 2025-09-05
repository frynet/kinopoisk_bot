from telebot.types import Message

from errors.handlers import user_friendly_errors
from loader import bot
from states.custom.search_by_name import search_by_name


@bot.message_handler(commands=["search_by_name"])
@user_friendly_errors
def bot_help(msg: Message):
    search_by_name(
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        msg_id=msg.message_id,
    )
