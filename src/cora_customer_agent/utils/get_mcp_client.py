from langchain_mcp_adapters.client import MultiServerMCPClient


def get_mcp_client() -> MultiServerMCPClient:
    """Creates and returns a MultiServerMCPClient configured to connect to the company MCP server.

    Returns:
        MultiServerMCPClient: An instance of MultiServerMCPClient configured for the company server.
    """
    return MultiServerMCPClient(
        {
            "company": {
                "transport": "streamable_http",
                "url": "http://localhost:8080/mcp",
            }
        }
    )
