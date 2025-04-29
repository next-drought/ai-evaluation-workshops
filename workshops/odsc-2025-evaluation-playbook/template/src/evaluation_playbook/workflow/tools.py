from langchain.tools.retriever import create_retriever_tool

from evaluation_playbook.config import settings
from evaluation_playbook.rag.retrievers import get_retriever

retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
    k=settings.RAG_TOP_K,
    device=settings.RAG_DEVICE,
)

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_philosopher_context",
    """
    Search and return information about a specific philosopher. Always use this tool when the user asks about facts about a philosopher's life, works, ideas, historical context or anything related to their life.

    For example, here are some example queries you can use this tool for:
    - When and where were you born? Also tell me more about your life, work and beliefs.
    - Tell me more about your life works and beliefs.
    - Tell me more about the Turing test.
    - What is the meaning of life? Does your work relate to this?
    - What is the historical context of your works?
    """,
)

tools = [retriever_tool]
