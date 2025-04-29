from langchain_qdrant import QdrantVectorStore
from loguru import logger

from evaluation_playbook.config import settings
from evaluation_playbook.domain.philosopher import PhilosopherExtract
from evaluation_playbook.qdrant_wrapper import QdrantClientWrapper
from evaluation_playbook.rag.deduplicate_documents import deduplicate_documents
from evaluation_playbook.rag.extract import get_extraction_generator
from evaluation_playbook.rag.splitters import Splitter, get_splitter


class LongTermMemoryCreator:
    """Creator class for building and managing long-term memory in a vector store.

    This class handles the process of creating and populating a vector store with
    philosopher extracts, including text splitting and deduplication.

    Attributes:
        database_client (QdrantClientWrapper): Client for managing Qdrant database operations.
        vector_store (QdrantVectorStore): Vector store for document storage and retrieval.
        splitter (Splitter): Text splitter for chunking documents.
    """

    def __init__(
        self,
        database_client: QdrantClientWrapper,
        vector_store: QdrantVectorStore,
        splitter: Splitter,
    ) -> None:
        """Initialize the LongTermMemoryCreator.

        Args:
            database_client (QdrantClientWrapper): Client for Qdrant operations.
            vector_store (QdrantVectorStore): Vector store instance.
            splitter (Splitter): Text splitter instance.
        """
        self.database_client = database_client
        self.vector_store = vector_store
        self.splitter = splitter

    @classmethod
    def build_from_settings(cls) -> "LongTermMemoryCreator":
        """Create a LongTermMemoryCreator instance using application settings.

        Returns:
            LongTermMemoryCreator: A configured instance using default settings
                for chunk size and vector store configuration.
        """

        qdrant_client = QdrantClientWrapper()
        splitter = get_splitter(chunk_size=settings.RAG_CHUNK_SIZE)

        return cls(qdrant_client, qdrant_client.vector_store, splitter)

    def __call__(self, philosophers: list[PhilosopherExtract]) -> None:
        """Process and store philosopher extracts in the vector store.

        Processes a list of philosopher extracts by:
        1. Clearing existing collection to avoid duplicates
        2. Extracting documents from philosophers
        3. Chunking documents using the configured splitter
        4. Deduplicating chunks with a similarity threshold
        5. Adding processed documents to the vector store

        Args:
            philosophers (list[PhilosopherExtract]): List of philosopher extracts to process.
        """

        if len(philosophers) == 0:
            logger.warning("No philosophers to extract. Exiting.")

            return

        # Clear the long term memory collection to avoid duplicates when re-running the script.
        self.database_client.clear_collection()

        extraction_generator = get_extraction_generator(philosophers)
        for _, docs in extraction_generator:
            chunked_docs = self.splitter.split_documents(docs)

            # TODO: (Module 2) Deduplicate documents
            # chunked_docs = deduplicate_documents(chunked_docs, threshold=0.5)

            self.vector_store.add_documents(chunked_docs)
