import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging(log_dir: str = "logs", service_name: str = "my-app"):
    """
    Configure Python logging with daily log rotation at midnight.

    - logs/<service_name>.log is rotated every day at 00:00
    - old logs receive a date suffix (e.g., my-app.log.2025-11-13)
    - backupCount controls how many rotated logs are kept

    Returns:
        logging.Logger: The root logger.
    """

    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{service_name}.log")

    # --- Formatter ---
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # --- Daily rotation handler ---
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",  # rotates daily at midnight
        interval=1,
        backupCount=14,  # keep 14 days of logs
        encoding="utf-8",
        utc=True,  # using UTC is recommended for services
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # --- Console handler ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # --- Root logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    root_logger.info("Daily rotating logging initialized at %s", log_file)

    return root_logger
