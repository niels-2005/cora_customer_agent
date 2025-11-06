from langchain_mcp_adapters.client import MultiServerMCPClient


def get_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "company_rag": {
                "transport": "stdio",
                "command": "uv",
                "args": ["run", "mcp", "run", "src/cora_customer_agent/mcp_server.py"],
            }
        }
    )


async def get_tools():
    mcp_client = get_mcp_client()
    tools = await mcp_client.get_tools()
    return tools
