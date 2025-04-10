#llm_service.py
from  langchain_openai import ChatOpenAI
from utils.logger import get_logger
from config.config import LLM_MODEL

logger = get_logger("LLM Service")

def content_refinement(chunk):
    """
    First tier: Use an LLM to generate an abstract representation of the document chunk.
    """
    logger.info("Refining content for the chunk.")
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = (
        "Summarize the essential information from the following text while "
        "preserving key relationships between concepts:\n\n" + chunk
    )
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content

def extract_triplets(text):
    """Extract entities and relationships using a chat-based LLM (e.g., GPT-4)."""
    logger.info("Extracting triplets from text.")
    
    # Initialize ChatOpenAI
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)  # Use the correct class for chat models
    
    # Format the input as a chat
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts entities and relationships in triplet format."},
        {"role": "user", "content": f"Extract entities and their relationships in triplet format (['head', 'head_type', 'relationship', 'object', 'object_type'] do not include these words, this is a template for your understanding) from the following text:\n\n{text}"}
    ]
    
    # Call the model
    response = llm.invoke(messages)
    
    logger.info("Triplets extracted: %s", response.content)
    return response.content