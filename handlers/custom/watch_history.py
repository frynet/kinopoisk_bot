from telebot.types import Message

from errors.handlers import user_friendly_errors
from loader import bot
from states.custom.watch_history import watch_history


@bot.message_handler(commands=["history"])
@user_friendly_errors
def bot_help(msg: Message):
    watch_history(
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        msg_id=msg.message_id,
    )
