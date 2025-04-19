from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from evaluation_playbook.workflow.nodes import (
    conversation_node,
    retriever_node,
)
from evaluation_playbook.workflow.state import PhilosopherState


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(PhilosopherState)

    graph_builder.add_node("conversation_node", conversation_node)
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
