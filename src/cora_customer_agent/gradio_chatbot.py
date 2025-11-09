from langchain.agents import create_agent

from pydantic import BaseModel
import gradio as gr

from cora_customer_agent.utils.load_ollama_llm import load_ollama_llm
from cora_customer_agent.utils.get_agent_tools import get_agent_tools
from cora_customer_agent.utils.get_agent_middleware import get_agent_middleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.cache import InMemoryCache

agent = create_agent(
    model=load_ollama_llm(),
    tools=get_agent_tools(),
    middleware=get_agent_middleware(),
    checkpointer=InMemorySaver(),
    cache=InMemoryCache(),
)


class UserContext(BaseModel):
    user_name: str


async def slow_echo(message, history):
    # Buffer für die komplette Antwort
    reasoning = ""
    full_response = ""

    async for token, metadata in agent.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config={"configurable": {"thread_id": "1"}},
        stream_mode="messages",
        context=UserContext(user_name="Niels"),
    ):
        # Tool-Outputs überspringen (haben 'name' und 'tool_call_id' Attribute)
        if hasattr(token, "tool_call_id") and token.tool_call_id:
            continue

        # Reasoning aus additional_kwargs verarbeiten
        if "reasoning_content" in token.additional_kwargs:
            reasoning += token.additional_kwargs["reasoning_content"]
            # yield reasoning  # Optional: Reasoning separat anzeigen

        # Normalen Text-Content verarbeiten
        if token.content:
            full_response += token.content
            yield full_response


gr.ChatInterface(
    fn=slow_echo,
    type="messages",
    textbox=gr.Textbox(
        placeholder="Ask me anything about TechHive", container=False, scale=7
    ),
    title="CORA - TechHive Customer Support Assistant",
    theme=gr.themes.Monochrome(),
).launch()
