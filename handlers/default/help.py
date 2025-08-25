from telebot.types import Message

from loader import bot
from texts import BOT_WHAT_CAN_I_DO
from utils.telegram import delete_message


@bot.message_handler(commands=["help"])
def bot_help(msg: Message) -> None:
    text = "ℹ️ Помощь\n\n" + BOT_WHAT_CAN_I_DO

    delete_message(bot, msg)

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
    )
