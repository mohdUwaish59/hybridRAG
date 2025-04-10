# main.py - Main pipeline for graph retrieval and context formatting
from services.neo4j_service import Neo4jService
from utils.logger import get_logger
import os
logger = get_logger("Main Pipeline")

def main():
    logger.info("Starting graph retrieval...")

    # Initialize Neo4j service
    neo4j_service = Neo4jService(
        uri=os.getenv("NEO4J_URI"),
        username="neo4j",
        password=os.getenv("NEO4J_PASSWORD"),
    )
    
    try:
        # Example: Retrieve context for a specific entity
        entity_name = "magmatism"
        logger.info("Retrieving subgraph context for entity: %s", entity_name)
        context = neo4j_service.retrieve_graph_context(query_entity=entity_name, depth=1)
        logger.info("Retrieved context: %s", context)

        # Example: Format context for downstream tasks (e.g., RAG pipeline)
        formatted_context = [
            f"{relation['subject']} {relation['predicate']} {relation['object']}"
            for relation in context['relations']
        ]
        logger.info("Formatted context: %s", formatted_context)

    finally:
        neo4j_service.close()


if __name__ == "__main__":
    main()
