from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from .get_agent_tools import get_tools
from .get_system_prompt import get_system_prompt
from .load_ollama_llm import load_ollama_llm


async def get_agent():
    tools = await get_tools()
    return create_agent(
        model=load_ollama_llm(),
        tools=tools,
        system_prompt=get_system_prompt(),
        checkpointer=InMemorySaver(),
    )
