from loguru import logger

from langchain_qdrant import QdrantVectorStore

from evaluation_playbook.qdrant_wrapper import QdrantClientWrapper
from evaluation_playbook.rag.deduplicate_documents import deduplicate_documents
from evaluation_playbook.rag.extract import get_extraction_generator
from evaluation_playbook.rag.splitters import Splitter, get_splitter
from evaluation_playbook.config import settings
from evaluation_playbook.domain.philosopher import PhilosopherExtract


class LongTermMemoryCreator:
    def __init__(
        self,
        database_client: QdrantClientWrapper,
        vector_store: QdrantVectorStore,
        splitter: Splitter,
    ) -> None:
        self.database_client = database_client
        self.vector_store = vector_store
        self.splitter = splitter

    @classmethod
    def build_from_settings(cls) -> "LongTermMemoryCreator":
        qdrant_client = QdrantClientWrapper()
        splitter = get_splitter(chunk_size=settings.RAG_CHUNK_SIZE)

        return cls(qdrant_client, qdrant_client.vector_store, splitter)

    def __call__(self, philosophers: list[PhilosopherExtract]) -> None:
        if len(philosophers) == 0:
            logger.warning("No philosophers to extract. Exiting.")

            return

        # Clear the long term memory collection to avoid duplicates when re-running the script.
        self.database_client.clear_collection()

        extraction_generator = get_extraction_generator(philosophers)
        for _, docs in extraction_generator:
            chunked_docs = self.splitter.split_documents(docs)

            chunked_docs = deduplicate_documents(chunked_docs, threshold=0.7)

            self.vector_store.add_documents(chunked_docs)
