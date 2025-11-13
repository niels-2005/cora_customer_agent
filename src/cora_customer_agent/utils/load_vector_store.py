from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from cora_customer_agent.cora_config import Config
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

_embedding_model = None


def load_company_docs(file_path: str) -> list[Document]:
    """
    Loads company documents from a JSON file.

    Note:
        The JSON file is expected to be an array of objects, each containing a 'content' key.

        For example:
                {
                    "id": 2,
                    "content": "Question: Which payment methods does TechHive accept?\nAnswer: We accept credit cards, PayPal, Klarna, instant bank transfer, Apple Pay, and Google Pay."
                }

    Args:
        file_path (str): Path to the JSON file containing documents.

    Returns:
        list: List of loaded documents.
    """
    try:
        loader = JSONLoader(
            file_path=file_path,
            jq_schema=".[]",
            content_key="content",
        )
        docs = loader.load()
        return docs
    except Exception as e:
        logger.error(
            f"Error loading company documents from {file_path}: {e}", exc_info=True
        )
        raise e


def load_embedding_model(model_name: str) -> HuggingFaceEmbeddings:
    """
    Loads or returns the cached HuggingFace embedding model.

    Note:
        Caching is needed to avoid re-initializing the model on each call.

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


def load_vector_store(
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
            embedding_function=load_embedding_model(
                Config.embedding_model_config["model_name"]
            ),
            host=Config.vector_db_config["host"],
            port=Config.vector_db_config["port"],
        )

        if init_vector_store:
            vector_store.add_documents(documents=load_company_docs(documents_json_path))

        return vector_store
    except Exception as e:
        logger.error(
            f"Error loading vector store {collection_name}: {e}", exc_info=True
        )
        raise e
