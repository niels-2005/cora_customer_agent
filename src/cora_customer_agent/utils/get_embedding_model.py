import logging

from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

_embedding_model = None


def get_embedding_model(model_name: str) -> HuggingFaceEmbeddings:
    """
    Loads or returns the cached HuggingFace embedding model.

    Note:
        The global variable _embedding_model is used to avoid re-initializing the model on each call.

    Args:
        model_name (str): Name of the HuggingFace model to load.

    Returns:
        HuggingFaceEmbeddings: The embedding model instance.
    """
    try:
        global _embedding_model
        if _embedding_model is None:
            _embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        return _embedding_model
    except Exception as e:
        logger.error(f"Error loading embedding model {model_name}: {e}", exc_info=True)
        raise e
