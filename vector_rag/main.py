# main.py - Main pipeline for vector retrieval and context formatting
from services.vector_rag_service_classify import VectorService
from config import CHROMADB_DIRECTORY, COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger("Main Pipeline")

def main():
    logger.info("Starting VectorRAG retrieval...")
    logger.debug(f"ChromaDB Directory: {CHROMADB_DIRECTORY}")
    logger.debug(f"Collection Name: {COLLECTION_NAME}")
    
    # Initialize the VectorService
    vector_service = VectorService()
    
    try:
        query = "How do sedimentary rocks form and evolve over time?"
        context = vector_service.retrieve_context(query=query, top_k=5)
        logger.info("Retrieved context: %s", context)
    except Exception as e:
        logger.error("Error in VectorRAG pipeline: %s", e)

if __name__ == "__main__":
    main()
