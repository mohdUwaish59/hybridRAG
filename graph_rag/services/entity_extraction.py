from  langchain_openai import ChatOpenAI

class EntityExtraction:
    def __init__(self):
        """
        Initialize Neo4jService for GraphRAG.
        """
    
    def extract_entities(self, query):
        """
        Use GPT-4 to extract entities from the query.
        Args:
            query (str): User's plain query.
        Returns:
            list: Extracted entities.
        """
        try:
            llm = ChatOpenAI(model="gpt-4", temperature=0)  # Use the correct class for chat models
    
            # Format the input as a chat
            messages = [
                {"role": "system", "content": "You are a helpful assistant that extracts entities from a text."},
                {"role": "user", "content": f"Extract entities from the following text:\n\n{query} and return response as a python list of entity or entities(If there are multiple)."}
            ]
            
            # Call the model
            response = llm.invoke(messages)
            print(response)
            #entities = response.choices[0].text.strip().split("\n")
            #entities = [entity.split(". ")[1] for entity in entities if ". " in entity]
            return response
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return []

ee = EntityExtraction()
print(ee.extract_entities("What are the geological features of the Earth with respect to moon?"))