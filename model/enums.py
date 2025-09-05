from __future__ import annotations

from datetime import timedelta
from enum import Enum


class HistoryPeriod(Enum):
    TODAY = "Сегодня"
    YESTERDAY = "Вчера"
    LAST_WEEK = "За неделю"
    LAST_MONTH = "За месяц"

    @property
    def days(self) -> int:
        return {
            HistoryPeriod.TODAY: 0,
            HistoryPeriod.YESTERDAY: 1,
            HistoryPeriod.LAST_WEEK: 7,
            HistoryPeriod.LAST_MONTH: 30,
        }[self]

    def get_range(self) -> timedelta:
        return timedelta(days=self.days)

    @classmethod
    def from_str(cls, name: str) -> HistoryPeriod | None:
        try:
            return cls[name]
        except KeyError:
            return None
