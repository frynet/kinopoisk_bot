from telebot.types import Message

from keyboards.inline.main_menu import create_main_menu
from keyboards.reply.global_menu import create_global_menu
from loader import bot
from services.users import user_service
from texts import BOT_WHAT_CAN_I_DO, BOT_WELCOME_TEXT, BOT_PRESS_TO_CONTINUE
from utils.telegram import delete_message


@bot.message_handler(commands=["start"])
def bot_start(msg: Message) -> None:
    user_service.get_or_create_user(msg.from_user)
    text = welcome_text(msg.from_user.full_name) + BOT_WHAT_CAN_I_DO

    delete_message(bot, msg)

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        reply_markup=create_global_menu(),
    )

    bot.send_message(
        chat_id=msg.chat.id,
        text=BOT_PRESS_TO_CONTINUE,
        reply_markup=create_main_menu(),
    )


def welcome_text(username: str) -> str:
    return f"Привет, {username}! 👋\n\n" + BOT_WELCOME_TEXT
