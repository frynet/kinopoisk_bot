from telebot.states import StatesGroup, State
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from loader import bot
from states.data_keys import (
    CUR_PAGE, MAX_PAGES, PAGE_SIZE,
    UPDATE_HANDLER, INITIAL_HANDLER,
)
from states.registry import execute_handler
from texts import (
    ERR_INVALID_PAGE_SIZE,
    BOT_PAGINATE_ALREADY_FIRST_PAGE_SELECT,
    BOT_PAGINATE_ALREADY_LAST_PAGE_SELECT,
)
from utils.callbacks import callback_match, Action, callback_parse
from utils.telegram import delete_message


class PaginationStates(StatesGroup):
    set_page_size = State()
    page_navigation = State()


@bot.callback_query_handler(
    func=callback_match(PaginationStates, [Action.SET_PAGE_SIZE])
)
def handle_page_size(
        call: CallbackQuery,
        state: StateContext,
):
    bot.answer_callback_query(call.id)

    data = callback_parse(call.data)
    page_size = data.payload.get("page_size")

    if not page_size or not page_size.isdigit():
        bot.answer_callback_query(call.id, ERR_INVALID_PAGE_SIZE, show_alert=True)

        return

    with state.data() as ctx:
        ctx[CUR_PAGE] = 1
        ctx[PAGE_SIZE] = int(page_size)

        handler = ctx.get(INITIAL_HANDLER)

    state.set(PaginationStates.page_navigation)
    delete_message(bot, call.message)

    if handler:
        execute_handler(handler, call.message.chat.id, state)


@bot.callback_query_handler(
    func=callback_match(PaginationStates, [Action.PREV_PAGE])
)
def handle_prev_page(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    with state.data() as ctx:
        page = ctx.get(CUR_PAGE)

        if page <= 1:
            bot.answer_callback_query(
                call.id,
                text=BOT_PAGINATE_ALREADY_FIRST_PAGE_SELECT,
                show_alert=True,
            )

            return

        ctx[CUR_PAGE] = page - 1
        handler = ctx.get(UPDATE_HANDLER)

    if handler:
        execute_handler(handler, call.message.chat.id, state)


@bot.callback_query_handler(
    func=callback_match(PaginationStates, [Action.NEXT_PAGE])
)
def handle_next_page(call: CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    with state.data() as ctx:
        page = ctx.get(CUR_PAGE)
        max_pages = ctx.get(MAX_PAGES)

        if max_pages is not None and page >= max_pages:
            bot.answer_callback_query(
                call.id,
                text=BOT_PAGINATE_ALREADY_LAST_PAGE_SELECT,
                show_alert=True,
            )

            return

        ctx[CUR_PAGE] = page + 1
        handler = ctx.get(UPDATE_HANDLER)

    if handler:
        execute_handler(handler, call.message.chat.id, state)
