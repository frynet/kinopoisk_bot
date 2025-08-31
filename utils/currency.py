from typing import Union

SHOWN_CURRENCIES = ("$", "€", "₽")
ABBRS = (
    (1_000_000_000, "млрд"),
    (1_000_000, "млн"),
    (1_000, "тыс."),
)


def format_currency_value(
        num: Union[int, float, None],
        symbol: str,
) -> str | None:
    if num is None or symbol not in SHOWN_CURRENCIES:
        return None

    for threshold, abbr in ABBRS:
        if num >= threshold:
            value = round(num / threshold, 1)
            return f"{int(value) if value.is_integer() else value} {abbr}"

    return str(int(num))
