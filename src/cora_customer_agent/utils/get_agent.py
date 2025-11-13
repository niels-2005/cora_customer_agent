import logging

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .get_agent_middleware import get_agent_middleware
from .get_mcp_client import get_mcp_client
from .get_ollama_llm import get_ollama_llm

logger = logging.getLogger(__name__)


async def get_agent():
    """
    Creates and returns an AI agent with MCP tools, middleware, memory.

    Returns:
        Agent: The configured agent instance.
    """
    try:
        client = get_mcp_client()
        tools = await client.get_tools()
        return create_agent(
            model=get_ollama_llm(),
            tools=tools,
            middleware=get_agent_middleware(),
            checkpointer=InMemorySaver(),
        )
    except Exception as e:
        logger.error(f"Error creating agent: {e}", exc_info=True)
        raise e
