# HybridRAG

## Text Information Extraction System for Georock Research Papers

![HybridRAG System](https://imgur.com/placeholder/400/200)

## Overview

HybridRAG is an advanced Retrieval-Augmented Generation system designed specifically for extracting and reasoning with geochemical information from scientific literature. By integrating vector-based semantic retrieval with graph-based structured knowledge extraction, HybridRAG significantly improves the accuracy, relevance, and reasoning capabilities of information retrieval from complex scientific texts.

The system dynamically selects retrieval strategies based on query classification, enabling more precise and context-aware responses across a spectrum of query types, from explicit fact retrieval to complex reasoning tasks.

## Key Features

- **Query Classification**: Automatically categorizes queries into Explicit Facts, Implicit Reasoning, Hidden Rationale, or Interpretable Rationale to optimize retrieval strategy
- **VectorRAG**: Utilizes dense embeddings and similarity search for semantic text retrieval
- **GraphRAG**: Leverages knowledge graphs for structured relationship extraction and reasoning
- **Dynamic Retrieval Selection**: Applies the optimal retrieval method based on query characteristics
- **Context Fusion**: Merges semantic and structured knowledge for comprehensive response generation
- **Scientific Domain Adaptation**: Specifically optimized for geochemistry domain knowledge

## System Architecture

```
                       ┌───────────────────┐
                       │   User Query      │
                       └─────────┬─────────┘
                                 │
                       ┌─────────▼─────────┐
                       │ Query Classification│
                       └─────────┬─────────┘
                                 │
              ┌─────────────────┴───────────────┐
              │                                 │
    ┌─────────▼─────────┐           ┌──────────▼───────────┐
    │    VectorRAG      │           │      GraphRAG        │
    │ Semantic Retrieval │           │ Structured Retrieval │
    └─────────┬─────────┘           └──────────┬───────────┘
              │                                │
              └─────────────┬─────────────────┘
                            │
                ┌───────────▼─────────────┐
                │  Context Fusion         │
                └───────────┬─────────────┘
                            │
                ┌───────────▼─────────────┐
                │ Response Generation     │
                └───────────┬─────────────┘
                            │
                ┌───────────▼─────────────┐
                │      Response          │
                └───────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/username/HybridRAG.git
cd HybridRAG

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Neo4j (required for GraphRAG)
docker pull neo4j:latest
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

## Requirements

```
langchain>=0.0.267
openai>=1.3.0
neo4j>=5.11.0
chromadb>=0.4.15
grobid-client>=0.8.0
spacy>=3.7.0
sentence-transformers>=2.2.2
faiss-cpu>=1.7.4
matplotlib>=3.7.2
scikit-learn>=1.3.0
transformers>=4.34.0
ragas>=0.0.18
```

## Data Preprocessing

Before running the system, preprocess your corpus of geochemical research papers:

```bash
# Process PDFs and extract text
python src/preprocessing/extract_text.py --input_dir /path/to/pdfs --output_dir /path/to/output

# Clean and chunk text
python src/preprocessing/clean_and_chunk.py --input_dir /path/to/output --output_dir /path/to/chunks

# Generate embeddings
python src/preprocessing/generate_embeddings.py --input_dir /path/to/chunks --output_dir /path/to/embeddings

# Build knowledge graph
python src/graph/build_knowledge_graph.py --input_dir /path/to/chunks --neo4j_uri bolt://localhost:7687
```

## Usage

### Basic Query Interface

```python
from hybrid_rag import HybridRAG

# Initialize the system
system = HybridRAG(
    vector_db_path="path/to/chroma_db",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
    model_name="gpt-4"
)

# Query the system
response = system.query("What factors influence uranium isotope fractionation in sedimentary environments?")
print(response)
```

### Running the Web Interface

```bash
# Start the web interface
python app.py --host 0.0.0.0 --port 8000
```

Then open your browser and navigate to `http://localhost:8000`

## Query Examples

### Explicit Fact Retrieval
```
What is the isotopic fractionation of Uranium?
```

### Implicit Reasoning
```
How does mineral composition affect element diffusion?
```

### Hidden Rationale
```
Why do certain isotopes exhibit fractionation under pressure?
```

### Interpretable Rationale
```
What factors influence isotopic fractionation trends?
```

## Evaluation

HybridRAG has been rigorously evaluated against a baseline RAG system using the following metrics:

### Response Quality Metrics
- Factual Correctness
- Semantic Similarity
- Non-LLM String Similarity
- BLEU Score
- ROUGE Score

### Retrieval-Based Metrics
- Context Precision
- Context Recall
- Context Entities Recall
- Noise Sensitivity
- Faithfulness

To run the evaluation suite:

```bash
python src/evaluation/evaluate.py --hybrid_results path/to/hybrid_results --baseline_results path/to/baseline_results
```

## Performance Results

HybridRAG outperforms the baseline RAG system in:

- **Factual Correctness**: Higher accuracy in complex query responses
- **Semantic Similarity**: Better alignment with reference answers
- **Context Entities Recall**: More comprehensive entity retrieval
- **Noise Sensitivity**: Lower rate of incorrect claims
- **Faithfulness**: Stronger alignment between responses and retrieved contexts

For detailed performance metrics, see the [evaluation report](docs/evaluation_report.md).

## Project Structure

```
HybridRAG/
│
├── src/
│   ├── preprocessing/
│   │   ├── extract_text.py
│   │   ├── clean_and_chunk.py
│   │   └── generate_embeddings.py
│   │
│   ├── classification/
│   │   ├── query_classifier.py
│   │   └── train_classifier.py
│   │
│   ├── vector_rag/
│   │   ├── embedding_utils.py
│   │   └── vector_retriever.py
│   │
│   ├── graph_rag/
│   │   ├── entity_extraction.py
│   │   ├── triplet_formation.py
│   │   └── graph_retriever.py
│   │
│   ├── hybrid_rag/
│   │   ├── context_merger.py
│   │   └── response_generator.py
│   │
│   └── evaluation/
│       ├── evaluate.py
│       └── metrics.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── embeddings/
│   └── knowledge_graph/
│
├── models/
│   ├── classifier/
│   └── saved_models/
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── evaluation_analysis.ipynb
│
├── app/
│   ├── static/
│   ├── templates/
│   └── app.py
│
├── docs/
│   ├── evaluation_report.md
│   └── api_documentation.md
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_classification.py
│   ├── test_vector_rag.py
│   ├── test_graph_rag.py
│   └── test_hybrid_rag.py
│
├── requirements.txt
├── setup.py
└── README.md
```

## Future Work

- Integration of domain-specific geochemical ontologies
- Refinement of query classification models with reinforcement learning
- Optimization of retrieval fusion techniques
- Enhanced explainability and traceability of responses
- Expansion to additional scientific domains

## Citation

If you use HybridRAG in your research, please cite:

```
@report{uwaish2025hybridrag,
  title={Building a System for Text Information Extraction from Georock Research Papers},
  author={Uwaish, Mohd},
  institution={University of Göttingen},
  year={2025}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- University of Göttingen for research support
- Georock Database for providing the corpus of geochemical research papers
- Contributors to the open-source libraries used in this project
