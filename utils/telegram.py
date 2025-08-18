from telebot import TeleBot
from telebot.types import Message

from utils.logging import log


def delete_message(
    bot: TeleBot,
    msg: Message,
) -> None:
    try:
        bot.delete_message(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
        )
    except Exception as e:
        log.warning(f"Ошибка при удалении сообщения: {e}")
