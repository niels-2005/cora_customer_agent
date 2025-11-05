from mcp.server.fastmcp import FastMCP
from .utils.load_vector_store import load_vector_store

mcp = FastMCP("Customer Chatbot MCP Server")

vector_store = load_vector_store(collection_name="company_faq", init_vector_store=False)


@mcp.tool()
def get_company_info():
    """Provides information about the company, its vision, target audience, and unique selling points."""
    with open("company_info.txt", "r", encoding="utf-8") as file:
        return file.read()


@mcp.tool()
async def get_company_faq_answers(query: str) -> str:
    """
    Use this tool to answer customer questions based on the company's FAQ documents.

    Args:
        query (str): The customer's question.
    """
    results = await vector_store.asimilarity_search(query, k=1)

    return results[0].page_content


@mcp.tool()
def get_product_informations():
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
