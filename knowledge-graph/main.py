from services.vector_store_service import initialize_vector_store, fetch_documents
from services.llm_service import content_refinement, extract_triplets
from services.knowledge_graph_service import Neo4jService
from utils.logger import get_logger
import os, ast

logger = get_logger("Main Pipeline")


def parse_triplets(response_text):
    """
    Parse triplets from the LLM response by removing line numbers and formatting issues.
    Args:
        response_text (str): Raw response text from the LLM.
    Returns:
        list: Parsed triplets as lists of elements.
    """
    triplets = []
    try:
        # Split the response into lines and process each line
        for line in response_text.splitlines():
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith(tuple(str(i) for i in range(1, 1000))) and '.' in line:
                # Remove the line number and period
                line = line.split('.', 1)[1].strip()
            
            # Parse the triplet using ast.literal_eval to safely evaluate the list
            if line.startswith('[') and line.endswith(']'):
                triplet = ast.literal_eval(line)  # Converts string representation of list to Python list
                triplets.append(triplet)
    except Exception as e:
        logger.error("Error parsing triplets: %s", e)
    return triplets


def append_metadata_to_triplets(triplets, metadata):
    """
    Append metadata to each extracted triplet.
    """
    if not triplets:
        logger.warning("No triplets provided for metadata appending.")
        return []

    logger.info("Appending metadata to triplets.")
    triplets_with_metadata = []
    for triplet in triplets:
        try:
            # Ensure the triplet is in the expected format
            if len(triplet) != 5:
                logger.error("Invalid triplet format: %s", triplet)
                continue

            # Append metadata to the triplet
            triplets_with_metadata.append(triplet + [metadata])
        except Exception as e:
            logger.error("Error appending metadata to triplet: %s", e)
    return triplets_with_metadata



def main():
    logger.info("Starting the pipeline.")
    
    # Step 1: Initialize Vector Store
    persist_directory = "./chroma_langchain_db"
    collection_name = "georock_research_papers"
    vector_store = initialize_vector_store(collection_name, persist_directory)
    
    # Step 2: Fetch Documents from Vector Store
    fetched_docs = fetch_documents(vector_store)
    logger.info("Fetched %d documents from ChromaDB.", len(fetched_docs))
    
    # Step 3: Process Documents and Extract Triplets with Metadata
    all_triplets = []
    for doc in fetched_docs:
        try:
            logger.info("Processing document: %s", doc.metadata.get("title", "Unknown Title"))
            metadata = doc.metadata
            logger.info("Metadata for document: %s", metadata)

            # Refine content
            refined_content = content_refinement(doc.page_content)
            logger.info("Refined content: %s", refined_content[:200])

            # Extract and parse triplets
            triplets_response = extract_triplets(refined_content)
            logger.info("Raw triplets response: %s", triplets_response)

            parsed_triplets = parse_triplets(triplets_response)
            logger.info("Parsed triplets: %s", parsed_triplets)

            # Append metadata
            triplets_with_metadata = append_metadata_to_triplets(parsed_triplets, metadata)
            logger.info("Triplets with metadata: %s", triplets_with_metadata)

            all_triplets.extend(triplets_with_metadata)
        except Exception as e:
            logger.error("Error processing document: %s", e)

    # Step 4: Save Knowledge Graph to Neo4j Aura
    neo4j_service = Neo4jService(
        uri="neo4j+s://76617872.databases.neo4j.io",
        username="neo4j",
        password="8YOnIGe-iYHAX0u_C5qTH8eo9_lm5tkiA2eFCdLYmlg"
    )
    try:
        neo4j_service.save_triplets(all_triplets)
        logger.info("Knowledge graph saved to Neo4j Aura.")
    finally:
        neo4j_service.close()


if __name__ == "__main__":
    main()
