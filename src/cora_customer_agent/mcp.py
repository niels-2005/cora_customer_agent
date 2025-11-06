from mcp.server.fastmcp import FastMCP
from cora_customer_agent.utils.load_vector_store import load_vector_store

mcp = FastMCP("Customer Chatbot MCP Server")

vector_store_faq = load_vector_store(
    collection_name="company_faq", init_vector_store=False
)
vector_store_products = load_vector_store(
    collection_name="company_products", init_vector_store=False
)


@mcp.tool()
async def get_company_faq_answers(query: str) -> str:
    """
    Answers customer questions based on the company's FAQ documents.

    Use this tool for general inquiries about company policies, products, or services.
    It performs a similarity search and returns the most relevant FAQ answer.

    Args:
        query (str): The customer's question, e.g., 'How do I reset my password?'.

    Returns:
        str: The content of the most relevant FAQ answer.
    """
    results = await vector_store_faq.asimilarity_search(query, k=1)

    return results[0].page_content


@mcp.tool()
async def get_product_informations(query: str) -> str:
    """
    Provides product information to answer customer questions based on company product documents.

    Use this tool for detailed inquiries about specific products, features, or specifications.
    It performs a similarity search and returns the most relevant product information.

    Args:
        query (str): The customer's question, including product details, e.g., 'Tell me about the HiveSmart Light Bulb A60'.

    Returns:
        str: The content of the most relevant product information.
    """
    results = await vector_store_products.asimilarity_search(query, k=1)

    return results[0].page_content


if __name__ == "__main__":
    mcp.run(transport="stdio")
