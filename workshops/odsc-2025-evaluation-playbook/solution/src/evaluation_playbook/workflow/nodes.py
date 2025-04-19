from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from evaluation_playbook.workflow.state import PhilosopherState
from evaluation_playbook.workflow.tools import tools

from evaluation_playbook.config import settings
from evaluation_playbook.domain.prompts import PHILOSOPHER_CHARACTER_CARD


def get_philosopher_response_chain():
    assert settings.OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"

    model = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.7,
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


async def conversation_node(state: PhilosopherState, config: RunnableConfig):
    conversation_chain = get_philosopher_response_chain()

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
