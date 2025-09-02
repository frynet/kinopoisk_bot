from __future__ import annotations

from typing import Callable, Any

from telebot.states import StatesGroup

from utils.logging import log

__all__ = ["get_func", "get_name", "register", "run"]

RegisteredCallable = Callable[..., Any]
_REGISTRY: dict[str, RegisteredCallable] = {}


def get_name(flow: type[StatesGroup], name: str) -> str:
    return f"{flow.__name__}_{name}"


def get_func(key: str) -> RegisteredCallable | None:
    func = _REGISTRY.get(key)

    if not func:
        log.error(f"Функция '{key}' не найдена в реестре.")

    return func


def register(
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

    def decorator(func: RegisteredCallable) -> RegisteredCallable:
        _REGISTRY[get_name(flow, name)] = func

        return func

    return decorator


def run(key: str, *args, **kwargs) -> Any | None:
    func = get_func(key)

    if func:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f"Ошибка при выполнении функции '{key}': {e}")

    return None
