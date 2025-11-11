import yaml
from typing import Any


def load_yaml_config(file_path: str) -> Any:
    """Load a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The contents of the YAML file.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
