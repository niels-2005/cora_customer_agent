from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Customer Chatbot MCP Server")


@mcp.tool()
def get_company_info():
    """Provides information about the company, its vision, target audience, and unique selling points."""
    with open("company_info.txt", "r", encoding="utf-8") as file:
        return file.read()


@mcp.tool()
def get_company_faq_answers():
    pass


@mcp.tool()
def get_product_informations():
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
