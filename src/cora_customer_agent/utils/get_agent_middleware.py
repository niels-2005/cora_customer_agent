from langchain.agents.middleware import dynamic_prompt, ModelRequest, PIIMiddleware
from .get_system_prompt import get_system_prompt
import logging

logger = logging.getLogger(__name__)


@dynamic_prompt
def get_dynamic_system_prompt(request: ModelRequest) -> str:
    """Generates a dynamic system prompt for the agent.

    Note:
        This middleware assumes that the request's runtime context includes a 'user_name' attribute.
        If not, it defaults to 'TechHive Friend'.

        So make sure to pass for example context=UserContext(user_name="Niels") when calling the agent for a specific user.

    Args:
        request (ModelRequest): The model request containing user context.

    Returns:
        str: The system prompt customized with the user's name.
    """
    try:
        user_name = (
            request.runtime.context.user_name
            if request.runtime.context and hasattr(request.runtime.context, "user_name")
            else "TechHive Friend"
        )
        return get_system_prompt(user_name=user_name)
    except Exception as e:
        logger.error(f"Error generating dynamic system prompt: {e}", exc_info=True)
        raise e


def get_agent_middleware() -> list:
    """
    Returns a list of middleware for the agent, including dynamic prompts and PII protection.

    Returns:
        list: List of middleware functions.
    """
    try:
        return [
            get_dynamic_system_prompt,
            # If the user inputs 'My email is john.doe@example.com', it will be redacted to 'My email is [REDACTED]'.
            PIIMiddleware(
                "email",
                strategy="redact",
                apply_to_input=True,
            ),
            # If the user inputs 'My credit card number is 1234-5678-9012-3456', it will be masked to 'My credit card number is ****-****-****-3456'.
            PIIMiddleware(
                "credit_card",
                strategy="mask",
                apply_to_input=True,
            ),
        ]
    except Exception as e:
        logger.error(f"Error setting up agent middleware: {e}", exc_info=True)
        raise e
