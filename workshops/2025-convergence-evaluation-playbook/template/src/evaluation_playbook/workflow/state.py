from langgraph.graph import MessagesState


class PhilosopherState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the Philosopher and the user.

    Attributes:
        philosopher_context (str): The historical and philosophical context of the philosopher.
        philosopher_name (str): The name of the philosopher.
        philosopher_perspective (str): The perspective of the philosopher about AI.
        philosopher_style (str): The style of the philosopher.
    """

    philosopher_context: str
    philosopher_name: str
    philosopher_perspective: str
    philosopher_style: str


def state_to_str(state: PhilosopherState) -> str:
    if "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
PhilosopherState(philosopher_context={state["philosopher_context"]}, 
philosopher_name={state["philosopher_name"]}, 
philosopher_perspective={state["philosopher_perspective"]}, 
philosopher_style={state["philosopher_style"]}, 
conversation={conversation})
        """
