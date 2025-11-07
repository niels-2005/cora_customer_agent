from cora_customer_agent.utils.get_agent import get_agent
from pydantic import BaseModel
import gradio as gr

agent = get_agent()


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
