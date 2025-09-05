from telebot import TeleBot, custom_filters
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage

import config
from errors.global_errors import GlobalExceptionHandler
from filters.callbacks import CallbackQueryFilter
from utils.telegram import set_default_commands

storage = StateMemoryStorage()
bot = TeleBot(
    token=config.BOT_TOKEN,
    state_storage=storage,
    use_class_middlewares=True,
    parse_mode="HTML",
    exception_handler=GlobalExceptionHandler(),
)

set_default_commands(bot)

# necessary for state parameter in handlers
bot.setup_middleware(StateMiddleware(bot))

# necessary for state filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(CallbackQueryFilter())
