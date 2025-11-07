from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from .get_agent_tools import get_tools
from .load_ollama_llm import load_ollama_llm
from .get_agent_middleware import get_agent_middleware


def get_agent():
    return create_agent(
        model=load_ollama_llm(),
        tools=get_tools(),
        middleware=get_agent_middleware(),
        checkpointer=InMemorySaver(),
    )
