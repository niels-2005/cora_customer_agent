from langchain_mcp_adapters.client import MultiServerMCPClient
from cora_customer_agent.cora_config import Config


def get_mcp_client() -> MultiServerMCPClient:
    """Creates and returns a MultiServerMCPClient configured to connect to the company MCP server.

    Returns:
        MultiServerMCPClient: An instance of MultiServerMCPClient configured for the company server.
    """
    return MultiServerMCPClient(
        {
            "company": {
                "transport": "streamable_http",
                "url": Config.mcp_client_config["url"],
            }
        }
    )
