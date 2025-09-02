class AppError(Exception):
    def __init__(self, message: str | None = None):
        self.message = message or "Произошла ошибка"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
