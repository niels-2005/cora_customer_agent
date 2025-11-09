from mcp.server.fastmcp import FastMCP
from langchain_core.documents import Document
from cora_customer_agent.utils.load_vector_store import load_vector_store

mcp = FastMCP("CoraCustomerAgentMCP", port=8080)

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


@mcp.tool()
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


@mcp.tool()
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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
