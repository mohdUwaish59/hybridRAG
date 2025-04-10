import chromadb

# Initialize the client
client = chromadb.PersistentClient(path="./chroma_langchain_db")

# Get a reference to your collection
collection = client.get_collection("georock_research_papers")

# Get all items from the collection
all_items = collection.get()

# Print the results
print(all_items)