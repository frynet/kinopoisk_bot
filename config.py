import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("search_by_name", "Поиск по названию"),
    ("search_by_rating", "Поиск по рейтингу"),
    ("low_budget_movie", "Поиск фильмов/сериалов с низким бюджетом"),
    ("high_budget_movie", "Поиск фильмов/сериалов с высоким бюджетом"),
    ("history", "Просмотр истории запросов и поиска"),
)
