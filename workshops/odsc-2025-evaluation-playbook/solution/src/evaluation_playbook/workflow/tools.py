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
    "Search and return information about a specific philosopher. Always use this tool when the user asks you about a philosopher's life, works, ideas, historical context or anything related to their life.",
)

tools = [retriever_tool]
