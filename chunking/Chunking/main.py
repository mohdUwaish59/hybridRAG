import os
from embedder import GeorockPaperEmbedder
from dotenv import load_dotenv
from config.logger_config import get_logger

logger = get_logger(__name__)

def main():
    load_dotenv()
    mongo_uri = os.getenv("mongo_uri")
    db_name = os.getenv("mongo_db")
    collection_name = os.getenv("mongo_collection")

    logger.info("Starting paper processing...")
    embedder = GeorockPaperEmbedder(
        mongo_uri=mongo_uri,
        db_name=db_name,
        collection_name=collection_name
    )
    embedder.process_all_papers()
    logger.info("Paper processing completed.")

if __name__ == "__main__":
    main()
