# hybrid-rag.py: Unified Pipeline for RAG Retrieval and response generation
from services.vector_rag_service_classify import VectorService
from services.entity_extraction_service import EntityExtraction
from services.neo4j_service import Neo4jService
from utils.logger import get_logger
from response_generation import format_prompt, query_gpt4
from metrices.metrice import RAGMetricsEvaluator  # Importing the RAGMetricsEvaluator class
import os
# Initialize logger
logger = get_logger("Unified Pipeline")

def main():
    logger.info("Starting Unified RAG Retrieval...")

    # Initialize the services
    vector_service = VectorService()
    entiry_extraction_service = EntityExtraction()
    neo4j_service = Neo4jService(
        uri=os.getenv("NEO4J_URI"),
        username="neo4j",
        password=os.getenv("NEO4J_PASSWORD")
    )

    # Initialize the evaluator (replace with your actual LLM evaluator)
    evaluator_llm = None  # Replace with your LLM evaluator instance
    metrics_evaluator = RAGMetricsEvaluator(evaluator_llm)

    try:
        # Accept user query from terminal
        query = input("Enter your query: ")

        # Retrieve context from VectorRAG
        logger.info("Retrieving context from VectorRAG...")

        vector_context = vector_service.retrieve_context(query=query, top_k=5)
        logger.info("VectorRAG context retrieved: %s", vector_context)

        # Retrieve context from GraphRAG
        logger.info("Retrieving context from GraphRAG...")
        entities = entiry_extraction_service.extract_entities(query)
        print("--------------------------")
        print(entities)
        print("--------------------------")
        graph_context = neo4j_service.retrieve_graph_context(query_entities=entities, depth=1)
        logger.info("GraphRAG context retrieved: %s", graph_context)

        # Format graph context for consistency
        formatted_graph_context = [
            f"{relation['subject']} {relation['predicate']} {relation['object']}"
            for relation in graph_context['relations']
        ]

        # Combine both contexts
        combined_context = {
            "VectorRAG_Context": vector_context,
            "GraphRAG_Context": formatted_graph_context
        }
        
        prompt = format_prompt(query, combined_context)
        logger.info("Formatted Prompt:\n%s", prompt)
    
        # Step 2: Query GPT-4
        response = query_gpt4(prompt)
        logger.info("GPT-4 Response:\n%s", response)
        print("GPT-4 Response:\n", response)

        # Display the combined context
        logger.info("Combined Context: %s", combined_context)
        print("\n--- Combined Context ---")
        print(combined_context)

        # Compute metrics
        reference_entities = entities  # You may modify this to get the actual reference entities
        reference_contexts = formatted_graph_context  # You may modify this to get the actual reference contexts

        context_entities_recall = metrics_evaluator.compute_context_entities_recall(query, vector_context, reference_entities)
        context_precision = metrics_evaluator.compute_context_precision(query, vector_context, reference_contexts)
        context_recall = metrics_evaluator.compute_context_recall(query, vector_context, reference_contexts)
        faithfulness_score = metrics_evaluator.compute_faithfulness(query, response, vector_context)
        noisy_contexts = vector_context  # You can introduce some noise to evaluate sensitivity
        noise_sensitivity_score = metrics_evaluator.compute_noise_sensitivity(query, vector_context, noisy_contexts, reference_contexts)

        # Print the metric results
        print(f"Context Entities Recall: {context_entities_recall}")
        print(f"Context Precision: {context_precision}")
        print(f"Context Recall: {context_recall}")
        print(f"Faithfulness: {faithfulness_score}")
        print(f"Noise Sensitivity: {noise_sensitivity_score}")

    except Exception as e:
        logger.error("Error in Unified Pipeline: %s", e)

    finally:
        # Ensure Neo4j service is properly closed
        neo4j_service.close()

if __name__ == "__main__":
    main()
