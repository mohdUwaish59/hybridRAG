from langchain_openai import OpenAIEmbeddings
from config.logger_config import get_logger

logger = get_logger(__name__)

class EmbeddingService:
    def __init__(self):
        """
        Initialize the embedding service using OpenAI's model.
        """
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        logger.info("Initialized OpenAI Embedding Service with text-embedding-ada-002.")

    def generate_embeddings(self, texts):
        """
        Generate embeddings for a list of texts.
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.debug(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
