from langchain_ollama import ChatOllama


def load_ollama_llm() -> ChatOllama:
    """
    Loads and configures a ChatOllama model instance.

    Returns:
        ChatOllama: The configured Ollama chat model.
    """
    return ChatOllama(
        model="qwen3:14b",
        temperature=0.8,
        reasoning=False,
        num_predict=512,
        num_ctx=10000,
        validate_model_on_init=True,
        keep_alive=1000,
    )
