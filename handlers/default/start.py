from telebot.types import Message

from keyboards.inline.main_menu import create_main_menu
from keyboards.reply.global_menu import create_global_menu
from loader import bot
from services.users import user_service
from utils.telegram import delete_message
from .help import what_can_i_do


@bot.message_handler(commands=["start"])
def bot_start(msg: Message) -> None:
    user_service.get_or_create_user(msg.from_user)
    text = welcome_text(msg.from_user.full_name) + what_can_i_do()

    delete_message(bot, msg)

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        reply_markup=create_global_menu(),
    )

    bot.send_message(
        chat_id=msg.chat.id,
        text="Нажми, чтобы продолжить 👇",
        reply_markup=create_main_menu(),
    )


def welcome_text(username: str) -> str:
    return (
        f"Привет, {username}! 👋\n\n"
        "Я бот для поиска фильмов и сериалов 🎬\n"
        "Готов помочь тебе найти интересное кино!\n\n"
    )
