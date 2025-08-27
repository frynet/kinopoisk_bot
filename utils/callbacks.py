from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Any

from telebot.states import StatesGroup
from telebot.types import CallbackQuery

__all__ = [
    "Action",
    "CallbackData",
    "callback_gen",
    "callback_match",
    "callback_parse",
]

# Формат: <flow>|<action>|<payload>
# payload: key1=value1;key2=value2
SEP = "|"
PAYLOAD_SEP = ";"
PAYLOAD_KV_SEP = "="
ANY_FLOW = "Any"


class Action(Enum):
    SET_PAGE_SIZE = auto()
    MARK_WATCHED = auto()
    MARK_UNWATCHED = auto()
    PREV_PAGE = auto()
    NEXT_PAGE = auto()


@dataclass(
    frozen=True,
    slots=True,
)
class CallbackData:
    flow: str
    action: Action
    payload: dict[str, str]


def callback_gen(
        flow: type[StatesGroup] | None,
        action: str | Action,
        payload: dict[str, Any] | None = None,
) -> str:
    flow_name = flow.__name__ if flow else ANY_FLOW
    action_name = action.name if isinstance(action, Action) else action
    parts = [flow_name, action_name]

    if payload:
        payload_parts = (
            f"{key}{PAYLOAD_KV_SEP}{str(value)}"
            for key, value in payload.items()
        )

        parts.append(PAYLOAD_SEP.join(payload_parts))

    data = SEP.join(parts)

    assert len(data) <= 64
    return data


def callback_parse(data: str | None) -> CallbackData | None:
    try:
        flow, act_name, *rest = data.split(SEP, 2)
        payload = {}

        if rest:
            for pair in rest[0].split(PAYLOAD_SEP):
                if PAYLOAD_KV_SEP in pair:
                    key, val = pair.split(PAYLOAD_KV_SEP, 1)
                    payload[key] = val

        return CallbackData(flow, Action[act_name], payload)
    except (KeyError, ValueError, IndexError):
        return None


def callback_match(
        flow: type[StatesGroup] | None,
        actions: Iterable[Action],
):
    expected_flow = flow.__name__ if flow else ANY_FLOW

    def _predicate(call: CallbackQuery) -> bool:
        if not call.data:
            return False

        data = callback_parse(call.data or "")

        return (
                data is not None
                and data.flow == expected_flow
                and data.action in set(actions)
        )

    return _predicate
