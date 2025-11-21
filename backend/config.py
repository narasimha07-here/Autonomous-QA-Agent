import os
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HTML_DIR = os.path.join(DATA_DIR, "html_files")
SUPPORT_DOCS_DIR = os.path.join(ASSETS_DIR, "support_docs")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(SUPPORT_DOCS_DIR, exist_ok=True)
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "gemini-2.5-flash"
CHUNK_THRESHOLD = "standard_deviation"
RETRIEVAL_K = 5