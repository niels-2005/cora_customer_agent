from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import HFTextVectorizer


def get_semantic_cache() -> SemanticCache:
    """
    Creates and returns a semantic cache using Redis and HuggingFace vectorizer.

    Returns:
        SemanticCache: The configured semantic cache instance.
    """
    return SemanticCache(
        name="llmcache",
        redis_url="redis://localhost:6379",
        distance_threshold=0.05,
        vectorizer=HFTextVectorizer("sentence-transformers/all-MiniLM-L6-v2"),
        ttl=3600,
    )
