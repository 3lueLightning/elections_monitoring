import re
import json
import logging
import inspect

from pathlib import Path
from pydantic import BaseModel, ValidationError


class SetLogger:
    """
    Creates logger attribute with 2 optional handlers:
        * one to log to the console
        * one to log to a file
    :param name: logger name (typically __name__)
    :param level: general logger level
    """
    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self.name: str = name
        self.logger_lvl: int = level
        self.logger: logging.Logger = self._set_logger()

    @staticmethod
    def _set_format(handler: logging.Handler) -> None:
        formatter: logging.Formatter = logging.Formatter(
            fmt='{asctime} - {name} - {levelname}: {message}',
            datefmt="%Y/%m/%d %H:%M:%S",
            style="{"
        )
        handler.setFormatter(formatter)

    def _set_logger(self) -> logging.Logger:
        logger: logging.Logger = logging.getLogger(self.name)
        logger.setLevel(self.logger_lvl)
        return logger

    def to_console(self, level: int = logging.INFO) -> None:
        ch: logging.Handler = logging.StreamHandler()
        ch.setLevel(level)
        # add formatter to ch
        self._set_format(ch)
        # add ch to logger
        self.logger.addHandler(ch)

    def to_file(self, name: str | Path, level: int = logging.INFO):
        fh: logging.Handler = logging.FileHandler(name)
        fh.setLevel(level)
        # add formatter to ch
        self._set_format(fh)
        # add ch to logger
        self.logger.addHandler(fh)


def full_logger(
        level: int = logging.INFO,
        file_name: str = None,
        to_console: bool = True) -> logging.Logger:
    """
    Set up all the logging utilities
    level: the logigng level
    file_name: the name of the file to log to
    to_console: whether to log to the console
    """
    # this finds the name of the module that called this function
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    logger_name = caller_module.__name__ if caller_module else '__main__'
    
    # logging to console and files
    logger = SetLogger(logger_name, level)
    if to_console:
        logger.to_console(level) 
    if file_name:
        logger.to_file(file_name, level)

    return logger.logger


def list_all_sqlite_tables(cursor, table_name):
    cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table';
        """
    )
    return cursor.fetchall()


def get_table_ddl(cursor, table_name):
    cursor.execute(
        f"""
        SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';
        """
    )
    return cursor.fetchone()[0]


def safe_model_validate_json(x: str, model: BaseModel) -> BaseModel | None:
    """
    Safely loads a pydantic model from a json string, returning None if it fails
    """
    try:
        return model.model_validate_json(x)
    except ValidationError:
        return None


def safe_model_dumps(x: BaseModel) -> dict | None:
    try:
        return x.model_dump_json()
    except AttributeError:
        return None


def safe_json_loads(x: str) -> dict | None:
    """
    Safely loads a json string, returning None if it fails
    """
    try:
        return json.loads(x)
    except TypeError:
        return None


def escape_quotes_within_citation(text):
    def escape_quotes(match):
        citation_text = match.group(1)
        escaped_citation = citation_text.replace('"', r'\"')
        return f'"citation": "{escaped_citation}",'

    return re.sub(r'"citation": "(.*?)"\s*,', escape_quotes, text)
