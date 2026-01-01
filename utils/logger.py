import logging
import os
from datetime import datetime

# Shared handlers so all loggers write to same file
_file_handler = None
_console_handler = None
_log_filepath = None


def get_logger(name: str) -> logging.Logger:
    global _file_handler, _console_handler, _log_filepath

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Create handlers once
    if _file_handler is None:
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        log_filename = f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        _log_filepath = os.path.join(logs_dir, log_filename)

        _file_handler = logging.FileHandler(_log_filepath, encoding="utf-8")
        _file_handler.setLevel(logging.DEBUG)
        _file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(logging.INFO)
        _console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
        )

    logger.addHandler(_file_handler)
    logger.addHandler(_console_handler)

    return logger


def log_test_start(logger: logging.Logger, test_name: str, params: dict = None) -> None:
    logger.info(f"{'=' * 80}")
    logger.info(f"Starting test: {test_name}")
    if params:
        logger.info(f"Test parameters: {params}")
    logger.info(f"{'=' * 80}")


def log_test_end(logger: logging.Logger, test_name: str, status: str = "COMPLETED") -> None:
    logger.info(f"{'=' * 80}")
    logger.info(f"Test {test_name} {status}")
    logger.info(f"{'=' * 80}\n")


def log_assertion(logger: logging.Logger, expected, actual, assertion_message: str = "") -> None:
    msg = f"Assertion: Expected='{expected}', Actual='{actual}'"
    if assertion_message:
        msg += f" - {assertion_message}"
    logger.info(msg)
