from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI


openai_api_key = os.getenv("OPENAI_API_KEY")
class PipelineService:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.0):
        """
        Initialize the pipeline with the desired model and temperature.
        """
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    def generate_response(self, context, query):
        """
        Generate a response using the provided context and query.
        
        Args:
            context (str): The combined context from VectorRAG and GraphRAG.
            query (str): The user's query.
        
        Returns:
            str: The generated response.
        """
        # Define the prompt template
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""
            You are a highly knowledgeable assistant. Use the provided context to answer the query:
            
            Context:
            {context}
            
            Query:
            {query}
            
            Answer:
            """
        )
        
        # Create the chain with the LLM and prompt
        chain = LLMChain(llm=self.llm, prompt=prompt)

        # Generate the response
        response = chain.run({"context": context, "query": query})
        return response
