import logging
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def get_yaml_config(file_path: str) -> Any:
    """Load a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The contents of the YAML file.
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error loading YAML config from {file_path}: {e}", exc_info=True)
        raise e
