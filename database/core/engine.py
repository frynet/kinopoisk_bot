from sqlalchemy import create_engine

DB_URL = "sqlite:///./bot.db"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
)
