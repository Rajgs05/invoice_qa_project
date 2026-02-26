import os
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.node_parser import SentenceSplitter

# Load environment variables (.env for GROQ_API_KEY)
load_dotenv()


def build_query_engine(markdown_folder: str):
    """
    Builds a fresh in-memory RAG pipeline for the given markdown folder.
    No persistence. No cross-document memory.
    Designed for single-invoice Q&A sessions.
    """

    # Load Markdown documents
    documents = SimpleDirectoryReader(markdown_folder).load_data()

    #  Local embedding model (CPU friendly)
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    Settings.embed_model = embed_model

    #  Groq LLM (fast + reliable)
    llm = Groq(model="llama-3.1-8b-instant")
    Settings.llm = llm

    #  Optimized chunking for invoices
    parser = SentenceSplitter(
        chunk_size=500,        # Ideal for structured invoice sections
        chunk_overlap=50       # Prevents label-value splitting
    )

    # Build vector index (in-memory only)
    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[parser]
    )

    # Controlled retrieval
    query_engine = index.as_query_engine(
        similarity_top_k=5,      
        response_mode="compact"  
    )

    return query_engine