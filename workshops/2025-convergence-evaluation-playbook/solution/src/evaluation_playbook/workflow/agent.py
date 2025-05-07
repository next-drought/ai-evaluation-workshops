import uuid
from typing import Any, AsyncGenerator

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from loguru import logger
from opik.integrations.langchain import OpikTracer

from evaluation_playbook.domain.philosopher_factory import PhilosopherFactory
from evaluation_playbook.workflow.graph import create_workflow_graph
from evaluation_playbook.workflow.state import PhilosopherState


async def call(
    messages: str | list[str] | list[dict[str, Any]],
    philosopher_id: str,
    new_thread: bool = False,
) -> tuple[str, PhilosopherState]:
    """Run a conversation through the workflow graph.

    Args:
        messages (Union[str, List[str], List[Dict[str, Any]]]): Messages to start the conversation.
            Can be a single string, list of strings, or list of message dictionaries.
        philosopher_id (str): Unique identifier for the philosopher to converse with.
        new_thread (bool, optional): Whether to create a new conversation thread.
            Defaults to False.

    Returns:
        Tuple[str, PhilosopherState]: A tuple containing:
            - str: The content of the last message in the conversation.
            - PhilosopherState: The final state after running the workflow.

    Raises:
        RuntimeError: If there's an error running the conversation workflow.
    """

    philosopher_factory = PhilosopherFactory()
    philosopher = philosopher_factory.get_philosopher(philosopher_id)

    graph_builder = create_workflow_graph(stream_usage=False)

    try:
        graph = graph_builder.compile()

        thread_id = (
            philosopher_id if not new_thread else f"{philosopher_id}-{uuid.uuid4()}"
        )
        config = {
            "configurable": {"thread_id": thread_id},
            "callbacks": [OpikTracer(graph=graph.get_graph(xray=True))],
        }

        output_state = await graph.ainvoke(
            input={
                "messages": __format_messages(messages=messages),
                "philosopher_name": philosopher.name,
                "philosopher_perspective": philosopher.perspective,
                "philosopher_style": philosopher.style,
                "philosopher_context": "",
            },
            config=config,
        )

        last_message = output_state["messages"][-1]

        return last_message.content, PhilosopherState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e


async def stream(
    messages: str | list[str] | list[dict[str, Any]],
    philosopher_id: str,
    new_thread: bool = False,
) -> AsyncGenerator[str, None]:
    """Run a conversation through the workflow graph and stream responses.

    Args:
        messages (Union[str, List[str], List[Dict[str, Any]]]): Messages to start the conversation.
            Can be a single string, list of strings, or list of message dictionaries.
        philosopher_id (str): Unique identifier for the philosopher to converse with.
        new_thread (bool, optional): Whether to create a new conversation thread.
            Defaults to False.

    Yields:
        str: Content chunks from the AI responses as they are generated.

    Raises:
        RuntimeError: If there's an error running the conversation workflow.
    """

    philosopher_factory = PhilosopherFactory()
    philosopher = philosopher_factory.get_philosopher(philosopher_id)

    graph_builder = create_workflow_graph(stream_usage=True)

    try:
        graph = graph_builder.compile()

        thread_id = (
            philosopher_id if not new_thread else f"{philosopher_id}-{uuid.uuid4()}"
        )
        config = {
            "configurable": {"thread_id": thread_id},
            "callbacks": [OpikTracer(graph=graph.get_graph(xray=True))],
        }

        async for chunk in graph.astream(
            input={
                "messages": __format_messages(messages=messages),
                "philosopher_name": philosopher.name,
                "philosopher_perspective": philosopher.perspective,
                "philosopher_style": philosopher.style,
                "philosopher_context": "",
            },
            config=config,
            stream_mode="messages",
        ):
            if chunk[1]["langgraph_node"] == "conversation_node" and isinstance(
                chunk[0], AIMessageChunk
            ):
                yield chunk[0].content

    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e


def render_graph(file_name: str = "workflow_graph.png") -> None:
    """Render the workflow graph to a PNG file.

    Compiles the workflow graph and saves a visual representation in Mermaid format
    to a PNG file.

    Args:
        file_name (str, optional): Output file path for the rendered graph.
            Defaults to "workflow_graph.png".

    Note:
        The graph is rendered with XRay mode enabled to show additional details.
    """

    graph_builder = create_workflow_graph(stream_usage=False)
    graph = graph_builder.compile()

    mermaid_png = graph.get_graph(xray=True).draw_mermaid_png(max_retries=3)
    with open(file_name, "wb") as f:
        f.write(mermaid_png)

    logger.info(f"Graph rendered to `{file_name}`")


def __format_messages(
    messages: str | list[dict[str, Any]],
) -> list[HumanMessage | AIMessage]:
    """Convert various message formats to a list of LangChain message objects.

    Args:
        messages: Can be one of:
            - A single string message
            - A list of string messages
            - A list of dictionaries with 'role' and 'content' keys

    Returns:
        List[Union[HumanMessage, AIMessage]]: A list of LangChain message objects
    """

    if isinstance(messages, str):
        return [HumanMessage(content=messages)]

    if isinstance(messages, list):
        if not messages:
            return []

        if (
            isinstance(messages[0], dict)
            and "role" in messages[0]
            and "content" in messages[0]
        ):
            result = []
            for msg in messages:
                if msg["role"] == "user":
                    result.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    result.append(AIMessage(content=msg["content"]))
            return result

        return [HumanMessage(content=message) for message in messages]
