from pathlib import Path

from utils.constants import Logs

BASE_DIR = Path(__file__).resolve().parent.parent


def get_logs_dir():
    """Проверяет наличие директории для логов и создает, если отсутствует."""
    logs_dir = BASE_DIR / Logs.DIR_NAME
    logs_dir.mkdir(exist_ok=True)
    return logs_dir
