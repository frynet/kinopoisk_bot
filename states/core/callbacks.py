from telebot.callback_data import CallbackData

from states.core.data_keys import (
    CB_ACTION,
    PAGE, PAGE_SIZE,
    MOVIE_TYPE, MOVIE_GENRE, MOVIE_RATING,
)


def cb_data(
        prefix: str,
        *,
        expect: list[str] | None = None,
) -> CallbackData:
    expect = expect or []

    if expect:
        prefix += "_" + "_".join(expect)

    return CallbackData(
        *expect,
        prefix=prefix,
    )


PAGINATION_PREFIX = "page"
PAGINATION_SET_SIZE = cb_data(PAGINATION_PREFIX, expect=[PAGE_SIZE])
PAGINATION_NAV_PAGE = cb_data(PAGINATION_PREFIX, expect=[CB_ACTION])

SEARCH_MOVIES_PREFIX = "find_mov"
MOVIE_SET_TYPE = cb_data(SEARCH_MOVIES_PREFIX, expect=[MOVIE_TYPE])
MOVIE_SET_GENRE = cb_data(SEARCH_MOVIES_PREFIX, expect=[MOVIE_GENRE])
MOVIE_NAV_GENRE = cb_data(SEARCH_MOVIES_PREFIX, expect=[CB_ACTION, PAGE])

RATING_FLOW_PREFIX = "find_by_rate"
RATING_FLOW_SET_RATE = cb_data(RATING_FLOW_PREFIX, expect=[MOVIE_RATING])
