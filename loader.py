from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config import config

storage = StateMemoryStorage()
bot = TeleBot(
    token=config.BOT_TOKEN,
    state_storage=storage,
)
