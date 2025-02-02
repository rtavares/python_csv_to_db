import logging
import logging.config
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    TABLE_NAME = os.getenv("TABLE_NAME")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_EXTERNAL_PORT")
    INPUT_FILE = os.getenv("INPUT_FILE")

    DEBUG = os.getenv("DEBUG")
    LOG_LEVEL = "WARNING"
    if DEBUG:
        LOG_LEVEL = "DEBUG"

    DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    def setup_logging(self):
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.LOG_LEVEL,
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "default",
                    "filename": "app.log",
                    "mode": "a",
                },
            },
            "loggers": {
                "app": {
                    "level": self.LOG_LEVEL,
                    "handlers": ["console", "file"],
                    "propagate": False,
                }
            },
            "root": {
                "level": self.LOG_LEVEL,
                "handlers": ["console"],
            },
        }

        logging.config.dictConfig(logging_config)
