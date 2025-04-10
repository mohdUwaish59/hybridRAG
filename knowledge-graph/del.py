import chromadb


client = chromadb.PersistentClient(path="./chroma_langchain_db")
collection_name = "georock_research_papers"

# Ensure the collection exists
try:
    collection = client.get_collection(name=collection_name)
except Exception as e:
    print(f"Error retrieving collection: {e}")
    exit()

# Fetch all items from the collection
try:
    all_items = collection.get()
    all_ids = all_items.get('ids', [])  # Safely get 'ids' from the result

    # If there are more than 10 items, identify the ones to delete
    if len(all_ids) > 1:
        ids_to_keep = all_ids[:1]  # Keep the first 10 items (or any specific logic)
        ids_to_delete = all_ids[1:]  # Delete the rest

        # Perform the deletion
        collection.delete(ids=ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} items. Kept 10 items in the collection.")
    else:
        print("Collection already has 10 or fewer items. No deletion required.")
except Exception as e:
    print(f"Error processing items in the collection: {e}")