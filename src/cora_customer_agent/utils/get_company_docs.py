import logging

from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def get_company_docs(file_path: str) -> list[Document]:
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
