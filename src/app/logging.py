import os
import logging


LEVEL_MAP = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "warning": logging.WARNING,
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "fatal": logging.FATAL,
}
LOG_LEVEL = LEVEL_MAP.get(os.getenv("API_LOG_LEVEL"), logging.INFO)


def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


api_logger = get_logger(os.getenv("PROJECT_NAME") or "api")
