from langchain_ollama import ChatOllama
from cora_customer_agent.cora_config import Config


def load_ollama_llm() -> ChatOllama:
    """
    Loads and configures a ChatOllama model instance.

    Returns:
        ChatOllama: The configured Ollama chat model.
    """
    return ChatOllama(**Config.ollama_config)
