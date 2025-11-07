from .load_vector_store import load_vector_store
from langchain.tools import tool, BaseTool
from langchain_core.documents import Document

vector_store_faq = load_vector_store(
    collection_name="company_faq",
    init_vector_store=False,
    documents_json_path="/home/ubuntu/dev/cora_customer_agent/company_faq.json",
)
vector_store_products = load_vector_store(
    collection_name="company_products",
    init_vector_store=False,
    documents_json_path="/home/ubuntu/dev/cora_customer_agent/company_products.json",
)


def get_tool_output(results: list[tuple[Document, float]]) -> str:
    """Extracts the content from the most relevant document in the results.

    Note:
        If there are no relevant documents found, a message indicating this will be returned. This is customizable and will effect
        how the agent responds when no relevant information is found.

    Args:
        results (list[tuple[Document, float]]): A list of tuples containing documents and their relevance scores.

    Returns:
        str: The content of the most relevant document or a message indicating no information was found.
    """
    if not results:
        return "No relevant information found."
    else:
        doc, score = results[0]
        return doc.page_content


@tool
async def get_company_faq_answers(query: str) -> str:
    """
    Answers customer questions based on the company's FAQ documents.

    Args:
        query (str): The customer's question, e.g., 'How do I reset my password?'.

    Returns:
        str: The content of the most relevant FAQ answer.
    """
    results = await vector_store_faq.asimilarity_search_with_relevance_scores(
        query, k=1, score_threshold=0.4
    )
    return get_tool_output(results)


@tool
async def get_product_informations(query: str) -> str:
    """
    Provides product information to answer customer questions based on company product documents.

    Args:
        query (str): The customer's question, including product details, e.g., 'Tell me about the HiveSmart Light Bulb A60'.

    Returns:
        str: The content of the most relevant product information.
    """
    results = await vector_store_products.asimilarity_search_with_relevance_scores(
        query, k=1, score_threshold=0.4
    )
    return get_tool_output(results)


def get_tools() -> list[BaseTool]:
    """
    Returns the list of tools available for the agent.

    Returns:
        list[BaseTool]: A list of tool functions for the agent.
    """
    return [get_company_faq_answers, get_product_informations]
