from typing import Any

from cora_customer_agent.utils.load_yaml_config import load_yaml_config


class CoraConfig:
    def __init__(
        self,
        config: Any = load_yaml_config("src/cora_customer_agent/cora_config.yaml"),
    ):
        """Initialize the CoraConfig class.

        Args:
            config (Any, optional): The configuration data. Defaults to load_yaml_config("src/cora_customer_agent/cora_config.yaml").
        """
        self.mcp_config = config["mcp_config"]
        self.mcp_client_config = config["mcp_client_config"]
        self.vector_db_config = config["vector_db_config"]
        self.embedding_model_config = config["embedding_model_config"]
        self.semantic_cache_config = config["semantic_cache_config"]
        self.ollama_config = config["ollama_config"]


Config = CoraConfig()
