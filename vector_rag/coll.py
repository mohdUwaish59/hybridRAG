import chromadb

def view_db_entries(path):
    client = chromadb.PersistentClient(path=path)
    collection_names = client.list_collections()
    
    for collection_name in collection_names:
        print(f"Collection: {collection_name}")
        db_collection = client.get_collection(collection_name)
        entries = db_collection.get(include=['documents', 'metadatas'])
        
        for i, (doc, metadata) in enumerate(zip(entries['documents'], entries['metadatas']), 1):
            print(f"  Entry {i}:")
            print(f"    Document: {doc[:200]}...")
            print(f"    Metadata: {metadata}\n")

if __name__ == "__main__":
    view_db_entries("./chroma_langchain_db")