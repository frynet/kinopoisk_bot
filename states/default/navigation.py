from telebot.apihelper import ApiTelegramException

from keyboards.inline.pagination import pagination_kb_text, pagination_kb
from loader import bot

__all__ = ["create_navigation"]


def create_navigation(
        page: int,
        pages: int,
        chat_id: int,
        nav_msg_id: int | None,
) -> int | None:
    text = pagination_kb_text(page, pages)
    keyboard = pagination_kb()

    send_new = lambda chat, txt, kb: bot.send_message(chat, txt, reply_markup=kb).message_id

    if nav_msg_id:
        try:
            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=nav_msg_id,
                reply_markup=keyboard,
            )
        except ApiTelegramException:
            return send_new(chat_id, text, keyboard)
    else:
        return send_new(chat_id, text, keyboard)

    return nav_msg_id
