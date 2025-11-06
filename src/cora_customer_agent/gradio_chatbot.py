from cora_customer_agent.utils.get_agent import get_agent
import gradio as gr
from gradio import ChatMessage

agent = None


async def slow_echo(message, history):
    global agent

    if agent is None:
        agent = await get_agent()

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
    ):
        for block in token.content_blocks:
            if "reasoning" in block:
                # Reasoning wird direkt yielded (kann separat behandelt werden)
                reasoning += block["reasoning"]
                # yield reasoning
            elif "text" in block:
                # Text zum Buffer hinzufügen
                full_response += block["text"]
                # Komplette Nachricht bis jetzt yielden
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
