import os
import shutil
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import config
from src.ingest import parse_pdf

def get_vectorstore():
    """
    Returns a Chroma vector store.
    - If DB exists, it loads it.
    - If DB is missing, it ingests the PDF, creates embeddings, and saves it.
    """
    embedding_function = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        api_key=config.OPENAI_API_KEY
    )

    # Checking if the DB already exists
    if os.path.exists(config.DB_DIR) and os.path.isdir(config.DB_DIR):
        print(f"--- Loading existing Vector Store from: {config.DB_DIR} ---")
        vectorstore = Chroma(
            persist_directory=config.DB_DIR,
            embedding_function=embedding_function
        )
    else:
        print(f"--- 🏗️ Creating NEW Vector Store at: {config.DB_DIR} ---")
        # Parsing PDF
        docs = parse_pdf()
        
        # Creating Vector Store
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embedding_function,
            persist_directory=config.DB_DIR
        )
        print("--- Vector Store Created & Persisted ---")

    return vectorstore

def reset_vectorstore():
    """Helper to clear the DB if you change ingestion logic."""
    if os.path.exists(config.DB_DIR):
        shutil.rmtree(config.DB_DIR)
        print("--- Vector Store Deleted ---")