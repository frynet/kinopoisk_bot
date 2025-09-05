import traceback

from telebot import ExceptionHandler

from utils.logging import log


class GlobalExceptionHandler(ExceptionHandler):
    def handle(self, ex):
        log.error("Unexpected error: {}\n{}", ex, traceback.format_exc())
