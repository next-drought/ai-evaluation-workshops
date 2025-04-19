from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from evaluation_playbook.qdrant_wrapper import QdrantClientWrapper


def get_retriever(
    embedding_model_id: str,
    k: int = 3,
    device: str = "cpu",
) -> VectorStoreRetriever:
    """Creates a Maximum Marginal Relevance (MMR) retriever using Qdrant vector store.

    This function initializes a Qdrant vector store client and configures it as a retriever
    using MMR search strategy for better diversity in retrieved documents.

    Args:
        embedding_model_id (str): The identifier for the embedding model to use for text embeddings.
            Example: "text-embedding-3-small".
        k (int, optional): Number of documents to retrieve in each search. Defaults to 3.
        device (str, optional): Computing device to run the embedding model on ('cpu' or 'cuda').
            Defaults to "cpu".

    Returns:
        VectorStoreRetriever: A configured retriever that performs MMR search over the Qdrant
            vector store.
    """

    logger.info(
        f"Initializing retriever | model: {embedding_model_id} | device: {device} | top_k: {k}"
    )

    qdrant_client = QdrantClientWrapper()

    return qdrant_client.vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": k}
    )


if __name__ == "__main__":
    retriever = get_retriever(
        embedding_model_id="text-embedding-3-small",
        k=3,
        device="cpu",
    )
    print(retriever.invoke("Where was Plato born?"))
