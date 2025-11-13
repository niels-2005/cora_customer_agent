from mcp.server.fastmcp import FastMCP
from langchain_core.documents import Document
from cora_customer_agent.utils.load_vector_store import load_vector_store
from cora_customer_agent.cora_config import Config
import logging

logger = logging.getLogger(__name__)

mcp = FastMCP(**Config.mcp_config)

vector_store_faq = load_vector_store(
    collection_name=Config.vector_db_config["faq_collection_name"],
    init_vector_store=Config.vector_db_config["init_vector_store"],
    documents_json_path=Config.vector_db_config["faq_json_path"],
)
vector_store_products = load_vector_store(
    collection_name=Config.vector_db_config["company_products_collection_name"],
    init_vector_store=Config.vector_db_config["init_vector_store"],
    documents_json_path=Config.vector_db_config["company_products_json_path"],
)


def get_tool_output(results: list[tuple[Document, float]]) -> str:
    """Extracts the content from the most relevant document in the results.

    Note:
        If there are no relevant documents found, a message indicating this will be returned. This is customizable and will probably affect
        how the agent responds when no relevant information is found.

        If something unexpected happens during processing, an error message will be returned and logged. The return message is customizable and will
        probably affect how the agent responds in case of errors.

    Args:
        results (list[tuple[Document, float]]): A list of tuples containing documents and their relevance scores.

    Returns:
        str: The content of the most relevant document or a message indicating no information was found.
    """
    try:
        if not results:
            return "No relevant information found."
        else:
            doc, score = results[0]
            return doc.page_content
    except Exception as e:
        logger.error(f"Error during getting the tool output: {e}", exc_info=True)
        return "Sorry, something went wrong while getting the tool output."


# If something unexpected happens during processing, an error message will be returned and logged.
# The return message is customizable and will probably affect how the agent responds in case of errors.
# Its commented outside the function to save tokens.
@mcp.tool()
async def get_company_faq_answers(query: str) -> str:
    """
    Answers customer questions based on the company's FAQ documents.

    Args:
        query (str): The customer's question, e.g., 'How do I reset my password?'.

    Returns:
        str: The content of the most relevant FAQ answer.
    """
    try:
        results = await vector_store_faq.asimilarity_search_with_relevance_scores(
            query,
            k=Config.vector_db_config["k"],
            score_threshold=Config.vector_db_config["score_threshold"],
        )
        return get_tool_output(results)
    except Exception as e:
        logger.error(f"Error during FAQ search: {e}", exc_info=True)
        return "Sorry, something went wrong while retrieving the FAQ information."


# If something unexpected happens during processing, an error message will be returned and logged.
# The return message is customizable and will probably affect how the agent responds in case of errors.
# Its commented outside the function to save tokens.
@mcp.tool()
async def get_product_informations(query: str) -> str:
    """
    Provides product information to answer customer questions based on company product documents.

    Args:
        query (str): The customer's question, including product details, e.g., 'Tell me about the HiveSmart Light Bulb A60'.

    Returns:
        str: The content of the most relevant product information.
    """
    try:
        results = await vector_store_products.asimilarity_search_with_relevance_scores(
            query,
            k=Config.vector_db_config["k"],
            score_threshold=Config.vector_db_config["score_threshold"],
        )
        return get_tool_output(results)
    except Exception as e:
        logger.error(f"Error during product information search: {e}", exc_info=True)
        return "Sorry, something went wrong while retrieving the product information."


def main():
    """Starts the MCP server with streamable HTTP transport."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
