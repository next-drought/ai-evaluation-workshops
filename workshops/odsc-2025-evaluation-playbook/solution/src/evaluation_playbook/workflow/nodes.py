from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from evaluation_playbook.config import settings
from evaluation_playbook.domain.prompts import PHILOSOPHER_CHARACTER_CARD
from evaluation_playbook.workflow.state import PhilosopherState
from evaluation_playbook.workflow.tools import tools


def get_philosopher_response_chain(stream_usage: bool = True):
    """Get the philosopher response chain.

    This function creates a chain of tools and a prompt for the philosopher response.
    It uses the OpenAI API to generate responses based on the philosopher's character card.

    Args:
        stream_usage: Whether to stream the usage of the OpenAI API.

    Returns:
        Runnable: A chain of tools and a prompt for the philosopher response.
    """

    assert settings.OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"

    model = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.7,
        stream_usage=stream_usage,
    )
    model = model.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PHILOSOPHER_CHARACTER_CARD.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
    )

    return prompt | model


retriever_node = ToolNode(tools)


async def conversation_node(
    state: PhilosopherState, config: RunnableConfig, stream_usage: bool = True
):
    """Conversation node for the philosopher workflow.

    This function processes the conversation state and invokes the philosopher response chain.
    It uses the OpenAI API to generate responses based on the philosopher's character card.

    Args:
        state: The current state of the conversation.
        config: The configuration for the conversation.
        stream_usage: Whether to stream the usage of the OpenAI API.
    Returns:
        dict: The updated state with the generated messages.
    """

    conversation_chain = get_philosopher_response_chain(stream_usage=stream_usage)

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "philosopher_context": state.get("philosopher_context", ""),
            "philosopher_name": state.get("philosopher_name", ""),
            "philosopher_perspective": state.get("philosopher_perspective", ""),
            "philosopher_style": state.get("philosopher_style", ""),
        },
        config,
    )

    return {"messages": response}
