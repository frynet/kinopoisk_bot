from functools import wraps
from typing import Callable, Any, Type

from requests import RequestException, HTTPError

from .logging import log


def log_request_error(error_cls: Type[Exception]):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except HTTPError as ex:
                response = ex.response

                log.opt(depth=1).error(
                    "HTTP error in {}: status={} url={} response={}",
                    func.__name__,
                    getattr(response, "status_code", "unknown"),
                    getattr(response, "url", "unknown"),
                    getattr(response, "text", "")[:500],
                )

                raise error_cls("External service error") from ex

            except (RequestException, ValueError) as ex:
                log.opt(depth=1).error(
                    "API request failed in {}: args={} kwargs={} err={}",
                    func.__name__, args, kwargs, ex,
                )

                raise error_cls("External service error") from ex

        return wrapper

    return decorator
