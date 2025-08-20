from functools import wraps
from typing import Callable, Any, Type

from requests import RequestException
from telebot.types import Message

from errors.api.kinopoisk import KinopoiskApiError
from loader import bot
from .logging import log

_FRIENDLY_ERROR_TEXT = (
    f"⚠️ Сервис временно недоступен."
    f"Мы уже знаем о проблеме и работаем над её решением 🙂"
)

_FRIENDLY_ERROR_KINOPOISK_TEXT = "😔 Кинопоиск сейчас недоступен, попробуйте позже."


def log_request_error(error_cls: Type[Exception]):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except (RequestException, ValueError) as ex:
                log.opt(depth=1).error(
                    "API request failed in {}: args={} kwargs={} err={}",
                    func.__name__, args, kwargs, ex,
                )

                raise error_cls("API request failed") from ex

        return wrapper

    return decorator


def user_friendly_errors(func):
    @wraps(func)
    def wrapper(msg: Message, *args, **kwargs):
        try:
            return func(msg, *args, **kwargs)
        except KinopoiskApiError:
            bot.send_message(msg.chat.id, _FRIENDLY_ERROR_KINOPOISK_TEXT)
        except Exception as ex:
            log.error("Unexpected error in handler {}: {}", func.__name__, ex)
            bot.send_message(msg.chat.id, _FRIENDLY_ERROR_TEXT)

    return wrapper
