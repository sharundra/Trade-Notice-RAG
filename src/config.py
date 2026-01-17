import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Path settings
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_PDF_PATH = os.path.join(DATA_DIR, "raw", "Trade_Notice_First_50_Pages.pdf")
    DB_DIR = os.path.join(DATA_DIR, "chroma_db")
    
    # Model settings
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o" 
    
    # Retrieval settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    K_RETRIEVAL = 5

    def validate(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in .env file")
        if not os.path.exists(self.RAW_PDF_PATH):
            raise FileNotFoundError(f"PDF not found at: {self.RAW_PDF_PATH}. Please place the file there.")

config = Config()