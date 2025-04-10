# services/embedding_service.py

from langchain.embeddings.openai import OpenAIEmbeddings
from utils.logger import get_logger

logger = get_logger("Embedding Service")

def generate_embedding(text):
    """Generate embeddings for the given text."""
    logger.info("Generating embedding for the text.")
    embedding_model = OpenAIEmbeddings()
    embedding = embedding_model.embed_query(text)
    logger.info("Embedding generated successfully.")
    return embedding
