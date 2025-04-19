from loguru import logger

from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


from evaluation_playbook.rag.embeddings import get_embedding_model
from evaluation_playbook.config import settings


class QdrantClientWrapper:
    """Wrapper class for managing Qdrant vector store operations.

    This class provides a simplified interface for working with Qdrant vector store,
    including collection management and vector store operations using LangChain integration.

    Attributes:
        client (QdrantClient): The underlying Qdrant client instance.
        vector_store (QdrantVectorStore): LangChain vector store interface for Qdrant.
    """

    def __init__(self) -> None:
        """Initialize the Qdrant client wrapper.

        Creates a connection to the Qdrant server and initializes the collection
        if it doesn't exist. Sets up the vector store with the specified embedding model.

        Raises:
            Exception: If there are issues connecting to Qdrant or creating the collection.
        """

        try:
            self.client = QdrantClient(url=settings.QDRANT_URL)
        except Exception as e:
            logger.error(f"Error initializing Qdrant client: {e}")
            raise e

        try:
            self.create_collection()
        except Exception as e:
            if f"`{settings.QDRANT_COLLECTION_NAME}` already exists" in str(e):
                logger.warning(
                    f"Qdrant collection `{settings.QDRANT_COLLECTION_NAME}` already exists. Skipping collection creation."
                )
            else:
                logger.error(f"Error initializing Qdrant client: {e}")
                raise e

        embeddings = get_embedding_model(
            model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            device=settings.RAG_DEVICE,
        )
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            embedding=embeddings,
            retrieval_mode=RetrievalMode.DENSE,
        )

    def create_collection(self) -> None:
        """Create a new Qdrant collection with the configured parameters.

        Creates a collection using the configured name and vector parameters from settings.
        The collection uses cosine distance for similarity calculations.

        Raises:
            Exception: If there are issues creating the collection.
        """

        self.client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.RAG_TEXT_EMBEDDING_MODEL_DIM, distance=Distance.COSINE
            ),
        )
        logger.info(f"Qdrant collection {settings.QDRANT_COLLECTION_NAME} created.")

    def clear_collection(self) -> None:
        """Clear all data from the Qdrant collection.

        Deletes the existing collection and creates a new empty one with the same parameters.
        This is useful for resetting the vector store state.
        """

        self.client.delete_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
        self.create_collection()
        logger.info(f"Qdrant collection {settings.QDRANT_COLLECTION_NAME} cleared.")
