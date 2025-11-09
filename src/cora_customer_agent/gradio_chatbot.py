from cora_customer_agent.utils.get_agent import get_agent
from cora_customer_agent.utils.get_semantic_cache import get_semantic_cache
from pydantic import BaseModel
import gradio as gr

_semantic_cache = get_semantic_cache()

_agent = None


class UserContext(BaseModel):
    user_name: str


async def generate_response(message, history):
    # Lazy load the agent, needed because get_agent is async.
    global _agent
    if _agent is None:
        _agent = await get_agent()

    # If Tokenizer available that supports async, switch to "await _semantic_cache.acheck(message)"
    cache_hit = _semantic_cache.check(message)
    if cache_hit:
        yield cache_hit[0]["response"]
        return

    full_response = ""

    async for token, metadata in _agent.astream(
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
        if hasattr(token, "tool_call_id") and token.tool_call_id:
            continue

        if token.content:
            full_response += token.content
            yield full_response

    if full_response.strip():
        # If Tokenizer availdable that supports async, switch to "await _semantic_cache.astore(...)"
        _semantic_cache.store(
            prompt=message,
            response=full_response,
        )


gr.ChatInterface(
    fn=generate_response,
    type="messages",
    textbox=gr.Textbox(
        placeholder="Ask me anything about TechHive", container=False, scale=7
    ),
    title="CORA - TechHive Customer Support Assistant",
    theme=gr.themes.Monochrome(),
).launch()
