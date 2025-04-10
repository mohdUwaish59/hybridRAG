import chromadb
from config.logger_config import get_logger

logger = get_logger(__name__)

class VectorStoreService:
    def __init__(self, collection_name="chunks"):
        """
        Initialize ChromaDB for storing embeddings.
        """
        try:
            self.client = chromadb.PersistentClient(path="./chroma/chroma_db")  # Persistent storage
            self.collection = self.client.get_or_create_collection(name=collection_name)
            logger.info(f"Initialized ChromaDB vector store: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to ChromaDB.
        """
        try:
            ids = [doc.metadata["chunk_id"] for doc in documents]
            texts = [doc.page_content for doc in documents]

            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=[doc.metadata for doc in documents],
                embeddings=embeddings
            )
            logger.info(f"Added {len(ids)} chunks to ChromaDB")
        except Exception as e:
            logger.error(f"Failed to add chunks to ChromaDB: {e}")
            raise
