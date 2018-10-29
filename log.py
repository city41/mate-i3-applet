import logging
import sys
from logging import handlers
from pathlib import Path


def exception_handler(type, value, traceback):
    logging.exception(
        "Uncaught exception occurred: {}"
        .format(value)
    )


def setup_logging():
    logger = logging.getLogger("")
    logger.setLevel(logging.WARNING)
    file_handler = handlers.TimedRotatingFileHandler(
        Path().home() / ".mate-i3-applet.log",
        when="D",
        backupCount=1,
        delay=True,
    )
    file_handler.setFormatter(
        logging.Formatter(
            '[%(levelname)s] %(asctime)s: %(message)s',
            "%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(file_handler)
    sys.excepthook = exception_handler
