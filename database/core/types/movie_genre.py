import json

from sqlalchemy.types import TypeDecorator, TEXT


class GenreListType(TypeDecorator):
    impl = TEXT
    cache_ok = True

    def process_bind_param(
            self,
            value: list[str] | None,
            dialect,
    ) -> str:
        return json.dumps(value or [], ensure_ascii=False)

    def process_result_value(
            self,
            value: str | None,
            dialect,
    ) -> list[str]:
        return json.loads(value) if value else []
