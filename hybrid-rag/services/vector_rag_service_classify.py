import os
import re
import pickle
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import MultiQueryRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from typing import List
import logging

CHROMADB_DIRECTORY = os.getenv("CHROMADB_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
CLASSIFICATION_MODEL_PATH = "./classification_model/classification_model.pkl"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VectorService")

class VectorService:
    def __init__(self):
        """
        Initialize the VectorService with ChromaDB, OpenAI embeddings, and classification model.
        """
        logger.info("Initializing VectorService...")
        
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        
        try:
            # Load classification model and category mapping
            logger.info("Loading classification model...")
            with open(CLASSIFICATION_MODEL_PATH, 'rb') as f:
                self.classification_model, self.category_mapping = pickle.load(f)
            logger.info("Classification model and mapping loaded successfully.")
            
            # Initialize OpenAI Embeddings
            self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            
            """# Initialize ChromaDB
            self.vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                persist_directory=CHROMADB_DIRECTORY,
                embedding_function=self.embeddings
            )"""
            
            # Initialize ChromaDB for streamlit
            self.vector_store = Chroma(
                collection_name="georock_research_papers",
                persist_directory="./chroma_langchain_db",
                embedding_function=self.embeddings
            )
            
            logger.info(f"Connected to ChromaDB collection: {COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize VectorService: {e}")
            raise e

    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocess the text: clean, stem, and remove stopwords.
        """
        stemmer = PorterStemmer()
        text = re.sub(r'\W+', ' ', text).strip().lower()
        tokens = [stemmer.stem(word) for word in text.split() if word not in stopwords.words('english')]
        return " ".join(tokens)

    def classify_query(self, query: str) -> str:
        """
        Classify query into predefined categories.
        
        Args:
            query (str): Input query text
        
        Returns:
            str: Predicted query category
        """
        try:
            # Preprocess query
            processed_query = self.preprocess_text(query)
            
            # Predict category
            predicted_label = self.classification_model.predict([processed_query])[0]
            logger.info(f"Predicted label: {predicted_label}")
            logger.info(f"Category mapping: {self.category_mapping}")
            
            # Map numerical label to category name
            category = {v: k for k, v in self.category_mapping.items()}[predicted_label]
            
            logger.info(f"Query classified as: {category}")
            return category
        
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return "default"
    


    def retrieve_context(self, query: str, top_k: int = 5) -> List[str]:
        """
        Dynamically retrieve context based on query classification.
        """
        try:
            category = self.classify_query(query)
            
            if category == "Explicit Fact":
                return self.simple_retrieval(query, top_k)
            elif category == "Implicit Fact":
                return self.multi_hop_retrieval(query, top_k)
            elif category == "Interpretable Rationale":
                return self.keyword_expansion_retrieval(query, top_k)
            elif category == "Hidden Rationale":
                return self.hybrid_retrieval(query, top_k)
            else:
                logger.warning("Default retrieval strategy used.")
                return self.simple_retrieval(query, top_k)
        except Exception as e:
            logger.error(f"Error during context retrieval: {e}")
            return []

    def simple_retrieval(self, query: str, top_k: int) -> List[str]:
        """
        Simple similarity search for explicit fact queries.
        """
        query_category = "Explicit Fact"
        logger.info("Performing simple similarity search.")
        retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.get_relevant_documents(query)
        return [doc.page_content for doc in docs]

    def multi_hop_retrieval(self, query: str, top_k: int) -> List[str]:
        """
        Multi-hop reasoning for implicit fact queries.
        """
        query_category = "Implicit Fact"
        logger.info("Performing multi-hop retrieval.")
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=self.vector_store.as_retriever(search_kwargs={"k": top_k}),
            llm=OpenAI(temperature=0)
        )
        docs = multi_query_retriever.get_relevant_documents(query)
        return [doc.page_content for doc in docs]

    def keyword_expansion_retrieval(self, query: str, top_k: int) -> List[str]:
        """
        Keyword-based expansion for interpretable rationale queries.
        """
        query_category = "Interpretable Rationale"
        logger.info("Performing keyword expansion retrieval.")
        
        # Expand the query using LLM
        expansion_prompt = f"""
        Expand the following search query with relevant keywords while preserving the original meaning.
        Original query: {query}
        Include synonyms and related terms that would help in retrieval.
        Return only the expanded query without explanations.
        """
        llm = OpenAI(temperature=0)
        expanded_query = llm.predict(expansion_prompt)
        logger.info(f"Expanded query: {expanded_query}")
        
        # Use the existing compression and retrieval logic with expanded query
        compressor = LLMChainExtractor.from_llm(OpenAI(temperature=0))
        retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=self.vector_store.as_retriever(search_kwargs={"k": top_k})
        )
        docs = retriever.get_relevant_documents(expanded_query)
        return [doc.page_content for doc in docs]

    def hybrid_retrieval(self, query: str, top_k: int) -> List[str]:
        """
        Hybrid retrieval combining sparse and dense methods for hidden rationale.
        """
        query_category = "Hidden Rationale"
        logger.info("Performing hybrid retrieval.")
        tools = [
            Tool(
                name="Chroma DB",
                func=lambda q: self.vector_store.similarity_search(q, k=top_k),
                description="Use this tool to retrieve specific facts from the vector DB."
            )
        ]
        agent = initialize_agent(tools, OpenAI(temperature=0), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        result = agent.run(query)
        return [result]

