from telebot.types import CallbackQuery

from loader import bot


class MovieService:
    def search_by_name(self, call: CallbackQuery) -> None:
        bot.send_message(call.message.chat.id, call.data)

    def search_by_rating(self, call: CallbackQuery) -> None:
        bot.send_message(call.message.chat.id, call.data)

    def search_low_budget(self, call: CallbackQuery) -> None:
        bot.send_message(call.message.chat.id, call.data)

    def search_high_budget(self, call: CallbackQuery) -> None:
        bot.send_message(call.message.chat.id, call.data)

    def show_history(self, call: CallbackQuery) -> None:
        bot.send_message(call.message.chat.id, call.data)


movie_service = MovieService()
