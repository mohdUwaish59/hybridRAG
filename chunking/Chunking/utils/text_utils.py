from langchain.text_splitter import TokenTextSplitter
from config.logger_config import get_logger

logger = get_logger(__name__)

class TextUtils:
    def __init__(self, encoding="gpt2", chunk_size=512, chunk_overlap=100):
        """
        Initialize the text utilities with a text splitter.
        """
        self.text_splitter = TokenTextSplitter(
            encoding_name=encoding,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        logger.info(f"Initialized text splitter with chunk_size={chunk_size} and chunk_overlap={chunk_overlap}.")

    def split_text(self, text):
        """
        Split text into smaller chunks.
        """
        try: 
            chunks = self.text_splitter.split_text(text)
            logger.debug(f"Split text into {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(f"Failed to split text: {str(e)}")
