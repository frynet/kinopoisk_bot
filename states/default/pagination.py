from telebot.states import StatesGroup, State
from telebot.states.sync import StateContext
from telebot.types import CallbackQuery

from loader import bot
from texts import (
    ERR_INVALID_PAGE_SIZE,
    BOT_PAGINATE_ALREADY_FIRST_PAGE_SELECT,
    BOT_PAGINATE_ALREADY_LAST_PAGE_SELECT,
)
from utils.callbacks import callback_match, Action, callback_parse
from ..core.data_keys import (
    CUR_PAGE, MAX_PAGES, PAGE_SIZE,
    DATA_GETTER_FUNC,
)
from ..core.registry import get_func
from ..core.renderers.movies import render_movies_page


class PaginationStates(StatesGroup):
    set_page_size = State()
    page_navigation = State()


@bot.callback_query_handler(
    func=callback_match(None, [Action.SET_PAGE_SIZE])
)
def select_page_size(
        call: CallbackQuery,
        state: StateContext,
):
    bot.answer_callback_query(call.id)

    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = callback_parse(call.data)
    page_size = data.payload.get("page_size")

    if not page_size or not page_size.isdigit():
        bot.answer_callback_query(call.id, ERR_INVALID_PAGE_SIZE, show_alert=True)

        return

    with state.data() as ctx:
        ctx[CUR_PAGE] = 1
        ctx[PAGE_SIZE] = int(page_size)

    state.set(PaginationStates.page_navigation)
    bot.delete_message(chat_id, msg_id)

    _render(chat_id, state)


@bot.callback_query_handler(
    func=callback_match(None, [Action.PREV_PAGE])
)
def nav_prev_page(
        call: CallbackQuery,
        state: StateContext,
):
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

    bot.answer_callback_query(call.id)
    _render(call.message.chat.id, state)


@bot.callback_query_handler(
    func=callback_match(None, [Action.NEXT_PAGE])
)
def nav_next_page(
        call: CallbackQuery,
        state: StateContext,
):
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

    bot.answer_callback_query(call.id)
    _render(call.message.chat.id, state)


def _render(chat_id: int, state: StateContext):
    with state.data() as ctx:
        data_getter = ctx.get(DATA_GETTER_FUNC)

    if data_getter and (data_getter_func := get_func(data_getter)):
        render_movies_page(
            chat_id, state,
            get_movies=data_getter_func(state),
        )
