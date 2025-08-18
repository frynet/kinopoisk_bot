import sys

from loguru import logger as log

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
    "[<cyan>{thread.name}</cyan>] "
    "<level>{level: <8}</level> "
    "<magenta>{name}</magenta>:"
    "<cyan>{function}</cyan>:"
    "<yellow>{line}</yellow> - "
    "<level>{message}</level>"
)

# drop default logger
log.remove()

log.add(
    sys.stdout,
    format=LOG_FORMAT,
)

log.add(
    "logs/bot.log",
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
    compression="gz",
    level="INFO",
    format=LOG_FORMAT,
)

__all__ = ["log"]
