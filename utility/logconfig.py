import logging
import logging.config
import colorlog

def init_log_conf():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s]%(reset)s %(message)s",
                "datefmt": "%Y-%m-%d/%H:%M:%S",
                "log_colors": {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'white,bg_red',
                },
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "DEBUG",
            }
        }
    })


def log_formatter(phase, identity):
    logs = phase
    for i in range(len(logs), 40):
        logs += " "
    return logs + identity

init_log_conf()
