from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")