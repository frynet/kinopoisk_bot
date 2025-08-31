from dataclasses import dataclass
from enum import Enum


@dataclass(
    frozen=True,
    slots=True,
)
class KinopoiskSlug:
    name: str
    slug: str


class SortType(str, Enum):
    ASC = "1"
    DESC = "-1"


class SortField(str, Enum):
    RATING_KINOPOISK = "rating.kp"
    RATING_IMDB = "rating.imdb"
    BUDGET = "budget.value"
