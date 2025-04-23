from functools import lru_cache, partial

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from evaluation_playbook.workflow.nodes import (
    conversation_node,
    retriever_node,
)
from evaluation_playbook.workflow.state import PhilosopherState


@lru_cache(maxsize=1)
def create_workflow_graph(stream_usage: bool = True) -> StateGraph:
    """Create a workflow graph for the philosopher conversation.

    This function constructs a StateGraph object that defines the flow of a conversation
    between a philosopher and a user. It includes nodes for conversation processing and
    retrieving philosopher context, and defines the sequence of operations to be executed.

    Args:
        stream_usage: Whether to stream the usage of the OpenAI API.

    Returns:
        StateGraph: A StateGraph object that defines the flow of the conversation.
    """

    graph_builder = StateGraph(PhilosopherState)

    graph_builder.add_node(
        "conversation_node", partial(conversation_node, stream_usage=stream_usage)
    )
    graph_builder.add_node("retrieve_philosopher_context", retriever_node)

    # Define the flow
    graph_builder.add_edge(START, "conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {"tools": "retrieve_philosopher_context", END: END},
    )
    graph_builder.add_edge("retrieve_philosopher_context", "conversation_node")

    return graph_builder
