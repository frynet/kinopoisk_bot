from loader import bot

if __name__ == "__main__":
    import states  # noqa
    import handlers  # noqa

    bot.infinity_polling(skip_pending=True)
