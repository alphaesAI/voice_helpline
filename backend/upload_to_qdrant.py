import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import Qdrant  # Updated import
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "helpline-docs")

# Initialize clients
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

vectorstore = Qdrant(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION,
    embeddings=embedding_model
)

# Get PDF file
pdf_path = input("Enter full PDF path: ").strip().strip('"')
if not os.path.exists(pdf_path):
    print("🚫 File not found.")
    exit()

print("📄 Loading and splitting document...")
loader = PyPDFLoader(pdf_path)  # Using the updated import
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = splitter.split_documents(pages)

print(f"✨ Embedding and uploading {len(docs)} chunks to Qdrant in batches...")

# Upload in smaller batches and with retries
BATCH_SIZE = 50
MAX_RETRIES = 3
for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i:i + BATCH_SIZE]
    retries = 0
    while retries < MAX_RETRIES:
        try:
            vectorstore.add_documents(batch)
            print(f"✅ Uploaded batch {i//BATCH_SIZE + 1}")
            break
        except Exception as e:
            retries += 1
            print(f"❌ Failed to upload batch {i//BATCH_SIZE + 1}: {e}")
            if retries < MAX_RETRIES:
                print(f"🔄 Retrying ({retries}/{MAX_RETRIES})...")
                time.sleep(5)  # Wait 5 seconds before retrying
            else:
                print("🚨 Maximum retries reached. Skipping batch.")

print("✅ Done.")
