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

    def retrieve_graph_context(self, query_entity, depth=1):
        """
        Retrieve a subgraph context around the specified entity using APOC.
        Args:
            query_entity (str): The starting entity for the retrieval.
            depth (int): The maximum depth of the subgraph.
        Returns:
            dict: A dictionary containing entities and relations in the subgraph.
        """
        with self.driver.session() as session:
            try:
                # Cypher query with APOC to retrieve the subgraph
                query = """
                MATCH (start {name: $entity})
                CALL apoc.path.subgraphAll(start, {
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
                
                result = session.run(query, entity=query_entity, depth=depth)
                
                # Process the results into a structured format
                context = {
                    'entities': set(),
                    'relations': []
                }
                
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
                logger.error("Error retrieving subgraph context for entity '%s': %s", query_entity, e)
                return {'entities': [], 'relations': []}
