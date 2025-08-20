from __future__ import annotations

from typing import List

from pydantic import BaseModel, HttpUrl, Field


class MovieGenreDto(BaseModel):
    name: str


class MoviePosterDto(BaseModel):
    url: HttpUrl | None = None


class MovieDto(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    year: int | None = None
    genres: List[MovieGenreDto] = Field(default_factory=list)
    age_rating: int | None = Field(default=None, alias="ageRating")
    poster: MoviePosterDto | None = None

    class Config:
        extra = "ignore"
        populate_by_name = True
