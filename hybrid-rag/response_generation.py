#response_generation

from  langchain_openai import ChatOpenAI
from utils.logger import get_logger
from langchain.schema import HumanMessage, SystemMessage  # For proper message formatting

logger = get_logger("Response Generation")


def format_prompt(query, combined_context):
    """
    Format the GPT-4 prompt using combined context.
    Args:
        query (str): The user query.
        combined_context (dict): Combined context from VectorRAG and GraphRAG.
    Returns:
        str: The formatted prompt.
    """
    vector_context = "\n\n".join(combined_context.get("VectorRAG_Context", []))
    graph_context = "\n\n".join(combined_context.get("GraphRAG_Context", []))
    
    prompt = f"""
    Use the following context to answer the query:

    Vector Context:
    {vector_context}

    Graph Context:
    {graph_context}

    Query:
    {query}
    
    Answer:
    """
    return prompt


def query_gpt4(prompt):
    """
    Query GPT-4 with the combined context prompt.
    Args:
        prompt (str): The formatted prompt.
    Returns:
        str: The GPT-4 response.
    """
    logger.info("Querying GPT-4...")
    try:
        # Initialize ChatOpenAI
        llm = ChatOpenAI(model="gpt-4", temperature=0)

        # Format the input as a chat
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=prompt)
        ]
        
        # Call the model
        response = llm(messages)
        logger.info("LLM Response:\n%s", response.content)
        return response.content.strip()
    except Exception as e:
        logger.error("Error querying GPT-4: %s", e)
        return "I'm sorry, but I couldn't generate a response."

    
    
