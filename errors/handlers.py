import traceback
from functools import wraps

from telebot.types import Message, CallbackQuery

from loader import bot
from texts import ERR_KINOPOISK_UNAVAILABLE, ERR_COMMON
from utils.logging import log
from .api.kinopoisk import KinopoiskApiError
from .app import AppError


def _find_context(args, wrapped_name: str) -> Message | CallbackQuery | None:
    for arg in args:
        if isinstance(arg, (Message, CallbackQuery)):
            return arg

    log.warning("{}: must contain one of [Message, CallbackQuery] in args", wrapped_name)
    return None


def user_friendly_errors(func):
    """
    Декоратор, который ловит ошибки в handlers и отправляет
    пользователю дружелюбное сообщение.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as ex:
            error_text = ex.message
        except KinopoiskApiError:
            error_text = ERR_KINOPOISK_UNAVAILABLE
        except Exception as ex:
            error_text = ERR_COMMON
            log.error("Unexpected error in '{}': {}\n{}", func.__name__, ex, traceback.format_exc())

        ctx = _find_context(args, func.__name__)
        if ctx:
            chat_id = ctx.chat.id \
                if isinstance(ctx, Message) \
                else ctx.message.chat.id

            if isinstance(ctx, CallbackQuery):
                bot.answer_callback_query(ctx.id)

            bot.send_message(chat_id, error_text)

        return None

    return wrapper
