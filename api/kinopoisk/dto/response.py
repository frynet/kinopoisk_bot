from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from model.movies import Movies
from .movie import MovieDto


class ResponseMovieSearch(BaseModel):
    movies: List[MovieDto] = Field(alias="docs", default_factory=list)
    total: int
    limit: int
    page: int
    pages: int

    class Config:
        extra = "ignore"

    def to_movies(self) -> Movies:
        return Movies(
            items=self.movies,
            page=self.page,
            pages=self.pages,
        )
