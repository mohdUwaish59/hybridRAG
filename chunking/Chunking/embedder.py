from services.mongo_service import get_mongo_collection
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from utils.text_utils import TextUtils
from langchain_core.documents import Document
from config.logger_config import get_logger
import time

logger = get_logger(__name__)

class GeorockPaperEmbedder:
    def __init__(self, mongo_uri, db_name, collection_name):
        """
        Load papers from MongoDB but store embeddings in ChromaDB.
        """
        self.collection = get_mongo_collection(mongo_uri, db_name, collection_name)  # Load from MongoDB
        self.embedding_service = EmbeddingService()
        self.text_utils = TextUtils()
        self.vector_store = VectorStoreService(collection_name="chunks")  # Save to ChromaDB

    def process_single_paper(self, paper):
        """
        Process a single paper document.
        """
        title = paper.get("metadata", {}).get("title", "Untitled Paper")
        paper_id = str(paper["_id"])
        logger.info(f"Starting to process paper: {title} (ID: {paper_id})")

        chunks = []
        texts = []  # Store raw texts for batch embedding

        for section in paper.get("sections", []):
            section_title = section.get("title", "Untitled Section")
            section_content = section.get("content", "")
            section_index = section.get("index", 0)

            if not section_content.strip():
                logger.debug(f"Skipping empty section: {section_title}")
                continue

            chunked_text = self.text_utils.split_text(section_content)
            logger.debug(f"Created {len(chunked_text)} chunks for section: {section_title}")

            for idx, chunk in enumerate(chunked_text):
                chunks.append(Document(
                    page_content=chunk,
                    metadata={
                        "paper_id": paper_id,
                        "title": title,
                        "section_title": section_title,
                        "chunk_index": idx,
                        "section_index": section_index,
                        "chunk_id": f"{paper_id}_chunk_{section_index}_{idx}",
                    }
                ))
                texts.append(chunk)

        if chunks:
            # Generate embeddings for all chunks at once
            embeddings = self.embedding_service.generate_embeddings(texts)
            # Store chunks and embeddings in ChromaDB
            self.vector_store.add_documents(chunks, embeddings)
            logger.info(f"Successfully processed {len(chunks)} chunks for paper: {title}")
        else:
            logger.warning(f"No chunks were generated for paper: {title}")

    def process_all_papers(self):
        """
        Load papers from MongoDB and process them.
        """
        start_time = time.time()
        paper_count = 0
        
        try:
            # Get total document count first
            total_docs = self.collection.count_documents({})
            logger.info(f"Found total {total_docs} documents in MongoDB")

            # Get a fresh cursor
            cursor = self.collection.find()

            for paper in cursor:
                try:
                    paper_id = str(paper.get('_id', 'Unknown ID'))
                    logger.info(f"Processing paper {paper_count + 1} of {total_docs} (ID: {paper_id})")

                    if not paper.get("sections"):
                        logger.warning(f"Skipping document {paper_id} due to missing 'sections'")
                        continue

                    self.process_single_paper(paper)
                    paper_count += 1

                    logger.info(f"Progress: {paper_count}/{total_docs} papers processed")

                except Exception as e:
                    logger.error(f"Error processing paper {paper_id}: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error during paper processing: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()

        elapsed_time = time.time() - start_time
        logger.info(f"Processing completed: {paper_count} out of {total_docs} papers processed in {elapsed_time:.2f} seconds")
