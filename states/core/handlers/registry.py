from __future__ import annotations

from typing import Callable

from telebot.states import StatesGroup
from telebot.states.sync import StateContext

from utils.logging import log

__all__ = ["get_key", "register_handler", "execute_handler"]

HandlerType = Callable[..., None]
_HANDLERS: dict[str, HandlerType] = {}


def get_key(flow: type[StatesGroup], name: str) -> str:
    return flow.__name__ + "_" + name


def register_handler(
        flow: type[StatesGroup],
        name: str,
):
    """
    Регистрирует функцию-обработчик в рамках указанного сценария.

    ================================================================
    WARNING: PRODUCTION ATTENTION
    ================================================================
    Не изменяйте параметр `name` после выхода бота в продакшн.

    Значение `name` сохраняется в пользовательском состоянии.
    Если его изменить, то все пользователи,
    находящиеся на этом этапе сценария, получат неработающие кнопки.

    ================================================================

    :param flow: Сценарий, к которому относится обработчик.
    :param name: Уникальное имя обработчика внутри указанного сценария.
    """

    def decorator(func: HandlerType) -> HandlerType:
        _HANDLERS[get_key(flow, name)] = func

        return func

    return decorator


def execute_handler(
        key: str,
        chat_id: int,
        state: StateContext,
        **kwargs,
):
    func = _HANDLERS.get(key)

    if func:
        try:
            func(chat_id, state, **kwargs)
        except Exception as e:
            log.error(f"Ошибка при выполнении обработчика '{key}': {e}")
    else:
        log.error(f"Обработчик для ключа '{key}' не найден в реестре.")
