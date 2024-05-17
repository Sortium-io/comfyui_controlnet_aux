#Cre: https://github.com/melMass/comfy_mtb/blob/main/log.py
import logging
import re
import os
import sys

base_log_level = logging.INFO


# Custom object that discards the output
class NullWriter:
    def write(self, text):
        pass


class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    purple = "\x1b[35;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "[%(name)s] | %(levelname)s -> %(message)s"

    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def mklog(name, level=base_log_level):
    logger = logging.getLogger()

    if not logger.handlers:
        logging_level = logging.INFO

        logger.setLevel(logging_level)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(message)s')
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)

        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

    return logger


# - The main app logger
log = mklog(__package__, base_log_level)


def log_user(arg):
    print("\033[34mComfyUI ControlNet AUX:\033[0m {arg}")


def get_summary(docstring):
    return docstring.strip().split("\n\n", 1)[0]


def blue_text(text):
    return f"\033[94m{text}\033[0m"


def cyan_text(text):
    return f"\033[96m{text}\033[0m"


def get_label(label):
    words = re.findall(r"(?:^|[A-Z])[a-z]*", label)
    return " ".join(words).strip()