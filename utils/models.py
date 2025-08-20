from pydantic import BaseModel


def get_required_fields(cls: type[BaseModel]) -> list[str]:
    return [
        field.alias or name
        for name, field in cls.model_fields.items()
    ]
