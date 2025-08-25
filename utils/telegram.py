from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove

from utils.logging import log


def delete_message(
        bot: TeleBot,
        msg: Message,
) -> None:
    delete_message_by_id(bot, msg.chat.id, msg.message_id)


def delete_message_by_id(
        bot: TeleBot,
        chat_id: int,
        msg_id: int,
) -> None:
    try:
        bot.delete_message(
            chat_id=chat_id,
            message_id=msg_id,
        )
    except Exception as e:
        log.warning(f"Ошибка при удалении сообщения: {e}")


def hide_reply_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
