from neo4j import GraphDatabase
from utils.logger import get_logger

logger = get_logger("Neo4j Service")

class Neo4jService:
    def __init__(self, uri, username, password):
        """
        Initialize the Neo4j database connection.
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    
    def close(self):
        """
        Close the database connection.
        """
        self.driver.close()

    def retrieve_graph_context(self, query_entities, depth=1):
        """
        Retrieve a subgraph context around the specified entities using substring matching and APOC.
        Args:
            query_entities (list): A list of entities to retrieve subgraphs for.
            depth (int): The maximum depth of the subgraph.
        Returns:
            dict: A dictionary containing entities and relations in the subgraph.
        """
        with self.driver.session() as session:
            try:
                # Prepare a context to collect results
                context = {
                    'entities': set(),
                    'relations': []
                }

                # Iterate over each entity in the list
                for query_entity in query_entities:
                    logger.info("Retrieving subgraph for entity containing: '%s'", query_entity)
                    
                    # Cypher query to match nodes containing the entity as a substring
                    query = """
                    MATCH (n)
                    WHERE n.name CONTAINS $entity
                    WITH n
                    CALL apoc.path.subgraphAll(n, {
                        maxLevel: $depth
                    }) 
                    YIELD nodes, relationships
                    UNWIND nodes AS node
                    UNWIND relationships AS rel
                    RETURN 
                        node.name AS entity_name, 
                        labels(node) AS entity_types,
                        type(rel) AS relationship_type,
                        startNode(rel).name AS start_node,
                        endNode(rel).name AS end_node
                    """
                    
                    # Execute the query for the current entity
                    result = session.run(query, entity=query_entity, depth=depth)
                    
                    # Process results
                    for record in result:
                        context['entities'].add(record['entity_name'])
                        if record['relationship_type']:
                            context['relations'].append({
                                'subject': record['start_node'],
                                'predicate': record['relationship_type'],
                                'object': record['end_node']
                            })
                
                # Convert the set of entities to a list
                context['entities'] = list(context['entities'])
                return context
            
            except Exception as e:
                logger.error("Error retrieving subgraph context: %s", e)
                return {'entities': [], 'relations': []}
