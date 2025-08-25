from __future__ import annotations

import textwrap
from typing import List

from pydantic import BaseModel, HttpUrl, Field


class MovieGenreDto(BaseModel):
    name: str


class MoviePosterDto(BaseModel):
    url: HttpUrl | None = None


class MovieRating(BaseModel):
    kp: float | None = None

class MovieDto(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    year: int | None = None
    genres: List[MovieGenreDto] = Field(default_factory=list)
    age_rating: int | None = Field(default=None, alias="ageRating")
    poster: MoviePosterDto | None = None
    rating: MovieRating | None = None

    class Config:
        extra = "ignore"
        populate_by_name = True

    def __str__(self):
        parts = [
            (
                f"<b>{self.name}</b>"
                f" ({self.year})" if self.year else ""
            )
        ]

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
