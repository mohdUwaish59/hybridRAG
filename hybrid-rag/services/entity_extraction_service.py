from langchain_openai import ChatOpenAI
from utils.logger import get_logger

logger = get_logger("Entity Extraction")

class EntityExtraction:
    def __init__(self):
        """
        Initialize the LLM for entity extraction.
        """
        try:
            self.llm = ChatOpenAI(model="gpt-4", temperature=0)  # Use GPT-4 for entity extraction
            logger.info("EntityExtraction initialized with GPT-4.")
        except Exception as e:
            logger.error("Failed to initialize EntityExtraction: %s", e)
            raise e

    def extract_entities(self, query):
        """
        Use GPT-4 to extract entities from the query.
        Args:
            query (str): User's plain query.
        Returns:
            list: Extracted entities as a list of strings.
        """
        try:
            logger.info("Extracting entities from query: %s", query)
            
            # Format the input as a chat
            messages = [
                {"role": "system", "content": "You are a helpful assistant that extracts entities from a text."},
                {"role": "user", "content": f"Extract entities from the following text:\n\n{query} and return response as a python list of entity or entities (if there are multiple)." }
            ]
            
            # Call the model
            response = self.llm.invoke(messages)
    
            # Extract response content
            response_text = response.content
            print(response_text)
            logger.info("LLM response: %s", response_text)
            
            # Evaluate the response content safely
            entities = eval(response_text) if isinstance(response_text, str) else []
            
            # Validate that the result is a list
            if not isinstance(entities, list):
                logger.warning("Unexpected LLM response format. Expected a list but got: %s", type(entities))
                return []
            
            logger.info("Extracted entities: %s", entities)
            return entities
        except Exception as e:
            logger.error("Error extracting entities: %s", e)
            return []
    
