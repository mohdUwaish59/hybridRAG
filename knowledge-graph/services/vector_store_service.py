#vector_store_service.py
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config.config import CHROMADB_COLLECTION_NAME, CHROMADB_DB_PATH
from utils.logger import get_logger

logger = get_logger("Vector Store Service")

def initialize_vector_store(collection_name=CHROMADB_COLLECTION_NAME, persist_directory=CHROMADB_DB_PATH):
    """Initialize ChromaDB vector store."""
    logger.info("Initializing ChromaDB vector store.")
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    logger.info("Vector store initialized for collection: %s", collection_name)
    return vector_store

def fetch_documents(vector_store):
    """Retrieve all documents from the vector store."""
    logger.info("Fetching documents from ChromaDB.")
    documents = vector_store.similarity_search("", k=1000)  # Fetch all documents
    logger.info("Retrieved %d documents.", len(documents))
    return documents


