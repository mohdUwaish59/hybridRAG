from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv(dotenv_path="../.env")  # Adjust the path based on your directory structure

# Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
