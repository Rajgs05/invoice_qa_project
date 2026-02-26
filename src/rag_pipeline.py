import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core import Settings
load_dotenv()

def build_query_engine(markdown_folder):
    documents = SimpleDirectoryReader(markdown_folder).load_data()

    # ✅ Use local embedding model (CPU friendly)
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Tell LlamaIndex to use this embedding model
    Settings.embed_model = embed_model

    # ✅ Groq LLM
    llm = Groq(model="llama-3.1-8b-instant")
    Settings.llm = llm

    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    return query_engine