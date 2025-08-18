from telebot.types import Message

from handlers.default.help import what_can_i_do
from keyboards.reply.global_menu import create_global_menu
from loader import bot
from utils.telegram import delete_message


@bot.message_handler(commands=["start"])
def bot_start(msg: Message) -> None:
    text = welcome_text(msg.from_user.full_name) + what_can_i_do()

    delete_message(bot, msg)

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        reply_markup=create_global_menu(),
    )


def welcome_text(username: str) -> str:
    return (
        f"Привет, {username}! 👋\n\n"
        "Я бот для поиска фильмов и сериалов 🎬\n"
        "Готов помочь тебе найти интересное кино!\n\n"
    )
