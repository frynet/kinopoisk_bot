from dataclasses import dataclass

from api.kinopoisk.dto.movie import MovieDto


@dataclass(
    frozen=True,
    slots=True,
)
class Movies:
    items: list[MovieDto]
    page: int
    pages: int
