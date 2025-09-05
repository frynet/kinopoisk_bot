from api.kinopoisk.dto.movie import MovieDto, MovieGenreDto, MoviePosterDto, MovieRating, MovieBudget
from database.dao import MovieDao


def dao_to_dto(dao: MovieDao) -> MovieDto:
    return MovieDto(
        id=dao.kinopoisk_id,
        name=dao.name,
        description=dao.description,
        year=dao.year,
        genres=[MovieGenreDto(name=g) for g in dao.genres],
        ageRating=dao.age_rating,
        poster=MoviePosterDto(url=dao.poster_url),
        rating=MovieRating(kp=dao.rating_kp, imdb=dao.rating_imdb),
        type=dao.type,
        budget=MovieBudget(
            value=dao.budget_value,
            currency=dao.budget_currency,
        ),
    )
