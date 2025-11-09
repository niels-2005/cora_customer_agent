from langchain_mcp_adapters.client import MultiServerMCPClient


def get_mcp_client() -> MultiServerMCPClient:
    """Creates and returns a MultiServerMCPClient configured to connect to the company MCP server.

    The client is set up to communicate with a remote MCP server over HTTP. Ensure that the
    company server is running on the specified URL and port before using this client.

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
