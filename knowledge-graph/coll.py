import chromadb

def view_db_entries(path):
    client = chromadb.PersistentClient(path=path)
    collection_names = client.list_collections()
    
    for collection_name in collection_names:
        print(f"Collection: {collection_name}")
        db_collection = client.get_collection(collection_name)
        entries = db_collection.get(include=['documents', 'metadatas'])
        print(entries)
        
        """for i, (doc, metadata) in enumerate(zip(entries['documents'], entries['metadatas']), 1):
            print(f"  Entry {i}:")
            print(f"    Document: {doc[:200]}...")
            print(f"    Metadata: {metadata}\n")"""

import chromadb
from typing import Dict, List, Optional

def inspect_collection_schema(collection_name: str, client: Optional[chromadb.Client] = None) -> Dict:
    """
    Inspect the schema of a ChromaDB collection.
    
    Args:
        collection_name (str): Name of the collection to inspect
        client (chromadb.Client, optional): ChromaDB client instance. If None, creates a new one.
        
    Returns:
        Dict: Dictionary containing collection metadata and schema information
    """
    # Create client if not provided
    if client is None:
        client = chromadb.Client()
    
    # Get the collection
    collection = client.get_collection(collection_name)
    
    # Get collection info
    count = collection.count()
    
    # Get a sample document to inspect schema
    results = collection.peek(limit=1)
    
    schema_info = {
        "collection_name": collection_name,
        "total_documents": count,
        "metadata": {
            "available": bool(results["metadatas"]),
            "sample": results["metadatas"][0] if results["metadatas"] else None
        },
        "embeddings": {
            "available": bool(results["embeddings"]),
            "dimension": len(results["embeddings"][0]) if results["embeddings"] else None
        },
        "documents": {
            "available": bool(results["documents"]),
            "sample": results["documents"][0] if results["documents"] else None
        }
    }
    
    return schema_info

if __name__ == "__main__":
    view_db_entries("./chroma_langchain_db_10")
    
    
    # Example usage
    client = chromadb.Client()
    schema = inspect_collection_schema("your_collection_name", client)
    
    # Print the schema information
    print(f"Collection: {schema['collection_name']}")
    print(f"Total documents: {schema['total_documents']}")
    print("\nMetadata:")
    print(f"  Available: {schema['metadata']['available']}")
    print(f"  Sample: {schema['metadata']['sample']}")
    print("\nEmbeddings:")
    print(f"  Available: {schema['embeddings']['available']}")
    print(f"  Dimension: {schema['embeddings']['dimension']}")
    print("\nDocuments:")
    print(f"  Available: {schema['documents']['available']}")
    print(f"  Sample: {schema['documents']['sample']}")