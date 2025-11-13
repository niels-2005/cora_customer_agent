import logging

from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import HFTextVectorizer

from cora_customer_agent.cora_config import Config

logger = logging.getLogger(__name__)


def get_semantic_cache() -> SemanticCache:
    """
    Creates and returns a semantic cache using Redis and HuggingFace vectorizer.

    Returns:
        SemanticCache: The configured semantic cache instance.
    """
    try:
        return SemanticCache(
            **Config.semantic_cache_config,
            vectorizer=HFTextVectorizer(
                model=Config.embedding_model_config["model_name"]
            ),
        )
    except Exception as e:
        logger.error(f"Error creating semantic cache: {e}", exc_info=True)
        raise e
