from __future__ import annotations

import textwrap
from enum import Enum
from typing import List, Any

from pydantic import BaseModel, HttpUrl, Field, field_validator

from utils.logging import log


class MovieGenreDto(BaseModel):
    name: str


class MoviePosterDto(BaseModel):
    url: HttpUrl | None = None


class MovieRating(BaseModel):
    kp: float | None = None


class MovieType(str, Enum):
    ANIMATED_SERIES = "animated-series"
    ANIME = "anime"
    CARTOON = "cartoon"
    MOVIE = "movie"
    TV_SERIES = "tv-series"

    @property
    def label(self) -> str:
        return {
            MovieType.ANIMATED_SERIES: "Анимационный сериал",
            MovieType.ANIME: "Аниме",
            MovieType.CARTOON: "Мультфильм",
            MovieType.MOVIE: "Фильм",
            MovieType.TV_SERIES: "Сериал",
        }.get(self, self.value)

    @classmethod
    def from_str(cls, value: str) -> MovieType | None:
        try:
            return cls(value)
        except ValueError:
            log.warning(f"[MovieType] Unknown type received: {value!r}")
            return None

class MovieDto(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    year: int | None = None
    genres: List[MovieGenreDto] = Field(default_factory=list)
    age_rating: int | None = Field(default=None, alias="ageRating")
    poster: MoviePosterDto | None = None
    rating: MovieRating | None = None
    type: MovieType | None = None

    class Config:
        extra = "ignore"
        populate_by_name = True

    @classmethod
    @field_validator("type", mode="before")
    def validate_type(cls, value: Any) -> MovieType | None:
        return MovieType.from_str(value) if isinstance(value, str) else value

    def __str__(self):
        parts = [
            (
                f"<b>{self.name}</b>"
                f" ({self.year})" if self.year else ""
            )
        ]

        if self.type:
            parts.append(f"🎬 <b>Тип:</b> {self.type.label}")

        if self.rating and self.rating.kp:
            parts.append(f"⭐️ <b>Кинопоиск:</b> {self.rating.kp:.1f}")

        meta = []
        if self.genres:
            genres = ", ".join(genre.name.capitalize() for genre in self.genres)
            meta.append(f"🎭 <b>Жанр:</b> {genres}")
        if self.age_rating is not None:
            meta.append(f"🔞 <b>Возраст:</b> {self.age_rating}+")
        if meta:
            parts.append("\n".join(meta))

        if self.description:
            desc = textwrap.shorten(
                self.description,
                width=400,
                placeholder="...",
            )
            parts.append(f"📝 <i>{desc}</i>")

        return "\n\n".join(parts)
