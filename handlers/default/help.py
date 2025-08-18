from telebot.types import Message

from loader import bot
from utils.telegram import delete_message


def what_can_i_do() -> str:
    return (
        "Вот что я умею:\n"
        "• 🔎 Поиск фильмов и сериалов по названию\n"
        "• ⭐ Поиск фильмов по рейтингу\n"
        "• 💰 Поиск фильмов по бюджету\n"
        "• 🕓 Просмотр истории твоего поиска\n\n"
        "Нажми, чтобы продолжить 👇"
    )


@bot.message_handler(commands=["help"])
def bot_help(msg: Message) -> None:
    text = "ℹ️ Помощь\n\n" + what_can_i_do()

    delete_message(bot, msg)

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
    )
