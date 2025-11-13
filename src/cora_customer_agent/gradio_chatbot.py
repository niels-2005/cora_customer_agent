import asyncio
from cora_customer_agent.utils.get_agent import get_agent
from cora_customer_agent.utils.get_semantic_cache import get_semantic_cache
from pydantic import BaseModel
import gradio as gr
from dotenv import load_dotenv
from .setup_logging import setup_logging
import logging

setup_logging(service_name="cora_customer_agent")

logger = logging.getLogger(__name__)

load_dotenv()

_semantic_cache = get_semantic_cache()

_agent = None


class UserContext(BaseModel):
    """User context for the chat session.

    Args:
        BaseModel (pydantic.BaseModel): Base model for data validation.
    """

    user_name: str


async def generate_response(message, history):
    """
    Generates a response to a user message using an AI agent with semantic caching.

    Args:
        message (str): The user's message, e.g., 'How do I reset my password?'.
        history (list): The chat history (not used in current implementation).

    Yields:
        str: Partial response content as tokens are generated.
    """
    try:
        # If Tokenizer available that supports async, switch to "await _semantic_cache.acheck(message)"
        cache_hit = _semantic_cache.check(message)
        if cache_hit:
            yield cache_hit[0]["response"]
            return

        full_response = ""

        # stream the response asynchronously back to the user
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
            context=UserContext(
                user_name="Niels"
            ),  # here you can change the user context, example: UserContext(user_name="Marc"), the Agent will respond accordingly
        ):
            # skip tool call tokens
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
    except Exception as e:
        logger.error(f"Error generating response: {e}", exc_info=True)
        yield "Sorry, something went wrong. Please try again later."


async def async_main():
    """Async main function to launch the Gradio chat interface with initializing the agent."""
    try:
        # needed because get_agent is async. In production, consider initializing with warmup sentences.
        global _agent
        if _agent is None:
            _agent = await get_agent()

        gr.ChatInterface(
            fn=generate_response,
            type="messages",
            textbox=gr.Textbox(
                placeholder="Ask me anything about TechHive", container=False, scale=7
            ),
            title="CORA - TechHive Customer Support Assistant",
            theme=gr.themes.Monochrome(),
        ).launch()
    except Exception as e:
        logger.error(f"Error launching Gradio interface: {e}", exc_info=True)


def main():
    """Synchronous entry point for the Gradio chatbot (called by script entry point)."""
    asyncio.run(async_main())
