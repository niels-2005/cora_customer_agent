from langchain_ollama import ChatOllama
from cora_customer_agent.cora_config import Config
import logging

logger = logging.getLogger(__name__)


def load_ollama_llm() -> ChatOllama:
    """
    Loads and configures a ChatOllama model instance.

    Returns:
        ChatOllama: The configured Ollama chat model.
    """
    try:
        return ChatOllama(**Config.ollama_config)
    except Exception as e:
        logger.error(f"Error loading Ollama LLM: {e}", exc_info=True)
        raise e
