from langchain.agents import create_agent
from .get_mcp_client import get_mcp_client

from .load_ollama_llm import load_ollama_llm
from .get_agent_middleware import get_agent_middleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.cache import InMemoryCache


client = get_mcp_client()


async def get_agent():
    """
    Creates and returns an AI agent with MCP tools, middleware, memory and caching.

    Returns:
        Agent: The configured agent instance.
    """
    return create_agent(
        model=load_ollama_llm(),
        tools=await client.get_tools(),
        middleware=get_agent_middleware(),
        checkpointer=InMemorySaver(),
        cache=InMemoryCache(),
    )
