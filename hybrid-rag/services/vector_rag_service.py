from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings  # Use the updated package
from utils.logger import get_logger
import os

CHROMADB_DIRECTORY = os.getenv("CHROMADB_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


logger = get_logger("Vector Service")

class VectorService:
    def __init__(self):
        """
        Initialize the ChromaDB vector store with the embedding function.
        """
        logger.info("Initializing VectorService...")
        logger.debug(f"ChromaDB Directory: {CHROMADB_DIRECTORY}")
        logger.debug(f"Collection Name: {COLLECTION_NAME}")
        
        try:
            logger.info("Connecting to ChromaDB...")
            
            # Initialize OpenAI Embeddings
            embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            
            # Connect to ChromaDB
            self.vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                persist_directory=CHROMADB_DIRECTORY,
                embedding_function=embeddings  # Provide the embedding function
            )
            
            logger.info("Connected to ChromaDB collection: %s", COLLECTION_NAME)
        except Exception as e:
            logger.error("Failed to connect to ChromaDB: %s", e)
            raise e

    def retrieve_context(self, query, top_k=5):
        """
        Retrieve the top-k most relevant chunks for the given query.
        Args:
            query (str): The query string.
            top_k (int): Number of top results to retrieve.
        Returns:
            list: A list of relevant document chunks.
        """
        try:
            logger.info("Retrieving context for query: %s", query)
            results = self.vector_store.similarity_search(query, k=top_k)
            context = [doc.page_content for doc in results]
            logger.info("Retrieved %d chunks.", len(context))
            return context
        except Exception as e:
            logger.error("Error during similarity search: %s", e)
            return []
