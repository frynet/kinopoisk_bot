from functools import wraps
from typing import Any
from urllib.parse import urlencode

from .logging import log


def log_http_request(func):
    @wraps(func)
    def wrapper(
            self,
            method: str,
            url: str,
            params: dict[str, Any] | None = None,
            *args, **kwargs,
    ):
        query = f"?{urlencode(params, doseq=True)}" if params else ""
        full_url = f"{url}{query}"

        log.info(f"[HTTP] {method.upper()} {full_url}")

        return func(self, method, url, params, *args, **kwargs)

    return wrapper
