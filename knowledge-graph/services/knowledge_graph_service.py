#knowledge_graph_service
from neo4j import GraphDatabase
import json
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

    def save_triplets(self, triplets):
        """
        Save triplets into Neo4j.
        Args:
            triplets (list): List of triplets in the format:
                ['head', 'head_type', 'relationship', 'object', 'object_type', 'metadata']
        """
        with self.driver.session() as session:
            for triplet in triplets:
                try:
                    head, head_type, relationship, obj, obj_type, metadata = triplet
                    metadata_str = json.dumps(metadata)  # Serialize metadata to JSON string
                    session.run("""
                        MERGE (h:Entity {name: $head, type: $head_type})
                        MERGE (o:Entity {name: $object, type: $object_type})
                        MERGE (h)-[r:RELATION {type: $relationship, metadata: $metadata}]->(o)
                    """, head=head, head_type=head_type, relationship=relationship,
                         object=obj, object_type=obj_type, metadata=metadata_str)
                except Exception as e:
                    logger.error("Error saving triplet to Neo4j: %s", e)
