import os
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "gemini-2.5-flash"
CHUNK_THRESHOLD = "standard_deviation"
RETRIEVAL_K = 5