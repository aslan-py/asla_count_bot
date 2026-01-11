import sys

from loguru import logger

from utils.constants import Logs
from utils.path_config import get_logs_dir


def setup_logging():
    """
    Настраивает логирование проекта: формат вывода, ротацию и хранение файлов.
    """
    logs_dir = get_logs_dir()
    logger.remove()

    logger.add(
        sink=sys.stdout,
        format=Logs.CONSOLE_FORMAT
    )
    logger.add(
        logs_dir / Logs.LOG_NAME,
        rotation=Logs.ROTATION,
        retention=Logs.RETENTION,
        level=Logs.LEVEL,
        format=Logs.FAIL_FORMAT,
        encoding=Logs.ENCODING
    )
