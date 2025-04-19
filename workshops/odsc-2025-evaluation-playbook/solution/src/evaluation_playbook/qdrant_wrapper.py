from loguru import logger

from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


from evaluation_playbook.rag.embeddings import get_embedding_model
from evaluation_playbook.config import settings


class QdrantClientWrapper:
    def __init__(self) -> None:
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
        self.client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.RAG_TEXT_EMBEDDING_MODEL_DIM, distance=Distance.COSINE
            ),
        )
        logger.info(f"Qdrant collection {settings.QDRANT_COLLECTION_NAME} created.")

    def clear_collection(self) -> None:
        self.client.delete_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
        self.create_collection()
        logger.info(f"Qdrant collection {settings.QDRANT_COLLECTION_NAME} cleared.")
