import os
import json
import re
from pymongo import MongoClient
from src.logger_config import get_logger

logger = get_logger()

class TextCleaner:
    def __init__(self, mongo_uri=None, mongo_db=None, mongo_collection=None):
        """
        Initialize the TextCleaner with MongoDB configuration.
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

        if not self.mongo_uri or not self.mongo_db or not self.mongo_collection:
            raise ValueError("MongoDB configuration is missing. Provide it explicitly or check environment variables.")

        # Initialize MongoDB client
        self.mongo_client = MongoClient(self.mongo_uri)
        self.mongo_db = self.mongo_client[self.mongo_db]
        self.mongo_collection = self.mongo_db[self.mongo_collection]

        logger.info(f"TextCleaner initialized with MongoDB collection: {self.mongo_db.name}.{self.mongo_collection.name}")

    def clean_section_text(self, text):
        """
        Cleans section text by removing references, excessive whitespace, and artifacts.
        """
        text = re.sub(r"\[\d+\]", "", text)  # Remove inline citations like [1]
        text = re.sub(r"\d+,", "", text)  # Remove dangling numbers like "18,"
        text = re.sub(r"\s*\n+\s*", " ", text)  # Replace newlines with spaces
        text = re.sub(r"\s{2,}", " ", text)  # Replace multiple spaces with one
        text = re.sub(r'\\u[0-9a-fA-F]{4}|Fig\.\s\d+[a-zA-Z]?', '', text)  # Remove Unicode sequences and "Fig. X"
        text = re.sub(r"[^\w\s.,;!?()-]", "", text)  # Remove unwanted symbols
        text = re.sub(r"\s+([.,;!?()-])", r"\1", text).strip()  # Fix spaces before punctuation
        return text

    def clean_and_save_to_mongo(self, json_data):
        """
        Cleans the 'sections' part of a JSON object, converts it to an indexed list, and saves the result to MongoDB.

        Args:
            json_data (dict): The JSON data to clean.

        Returns:
            dict: The cleaned JSON data.
        """
        try:
            sections = json_data.get("sections", {})
            cleaned_sections = []

            for index, (title, content) in enumerate(sections.items()):
                logger.info(f"Cleaning section {index + 1}: {title}")
                cleaned_content = self.clean_section_text(content)
                cleaned_sections.append({"index": index + 1, "title": title, "content": cleaned_content})

            # Replace sections with indexed list
            json_data["sections"] = cleaned_sections

            # Save the cleaned JSON to MongoDB
            logger.info("Saving cleaned JSON data to MongoDB...")
            self.mongo_collection.insert_one(json_data)
            logger.info("Cleaned JSON successfully saved to MongoDB.")
            return json_data

        except Exception as e:
            logger.error(f"Error cleaning and saving JSON data to MongoDB: {e}")
            return None
