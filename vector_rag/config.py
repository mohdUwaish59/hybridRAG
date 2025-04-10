from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv(dotenv_path="../.env")  # Adjust the path based on your directory structure

CLASSIFICATION_MODEL_PATH = "./classification_model/classification_model.pkl"
CHROMADB_DIRECTORY = os.getenv("CHROMADB_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")