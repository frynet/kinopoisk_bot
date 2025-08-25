from telebot.types import Message

from loader import bot
from texts import BOT_WHAT_CAN_I_DO
from utils.telegram import delete_message


@bot.message_handler(commands=["help"])
def bot_help(msg: Message) -> None:
    _prepare(msg)
    
    text = "ℹ️ Помощь\n\n" + BOT_WHAT_CAN_I_DO

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
    )


def _prepare(msg: Message) -> None:
    bot.delete_state(msg.from_user.id, msg.chat.id)
    delete_message(bot, msg)
