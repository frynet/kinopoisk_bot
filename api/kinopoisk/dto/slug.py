from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class KinopoiskSlug:
    name: str
    slug: str
