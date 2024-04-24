import logging
import logging.handlers
import os
from pathlib import Path

LOGS_DIR = str(Path.cwd()) + "/logs"


def create_logger(name, level=logging.DEBUG):
    """Создаёт логгер с заданными параметрами.

    Args:
        name (str): Имя логгера.
        level (int, optional): Уровень логирования. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Настроенный логгер.
    """
    # Создаём логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Создаём обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    log_file = os.path.join(LOGS_DIR, name + ".log")

    # Создаём обработчик для вывода в файл
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5
    )  # 10MB файл с 5 резервными копиями
    file_handler.setLevel(level)

    # Создаём форматеры
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Устанавливаем форматеры для обработчиков
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Добавляем обработчики к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
