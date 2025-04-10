from pymongo import MongoClient
from config.logger_config import get_logger

logger = get_logger(__name__)

def get_mongo_collection(mongo_uri, db_name, collection_name):
    """
    Connect to MongoDB and return the specified collection.
    """
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        logger.info(f"Connected to MongoDB: {db_name}/{collection_name}")
        return db[collection_name]
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
