import logging

from langchain_chroma import Chroma

from cora_customer_agent.cora_config import Config

from .get_company_docs import get_company_docs
from .get_embedding_model import get_embedding_model

logger = logging.getLogger(__name__)


def get_vector_store(
    collection_name: str,
    init_vector_store: bool = True,
    documents_json_path: str = None,
) -> Chroma:
    """
    Loads a Chroma vector store with optional document initialization.

    Note:
        If init_vector_store is True, documents will be loaded from the specified JSON file and added to the vector store.
        Use this option when setting up the vector store for the first time or when updating documents.

    Args:
        collection_name (str): Name of the collection.
        init_vector_store (bool): Whether to add documents to the store. Defaults to True.
        documents_json_path (str): Path to JSON file for documents if init_vector_store is True. Defaults to None.

    Returns:
        Chroma: The vector store instance.
    """
    try:
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=get_embedding_model(
                Config.embedding_model_config["model_name"]
            ),
            host=Config.vector_db_config["host"],
            port=Config.vector_db_config["port"],
        )

        if init_vector_store:
            vector_store.add_documents(documents=get_company_docs(documents_json_path))

        return vector_store
    except Exception as e:
        logger.error(
            f"Error loading vector store {collection_name}: {e}", exc_info=True
        )
        raise e
