from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from gemini import gemini_response
from qdrant_client import QdrantClient 
from qdrant_client.models import ScoredPoint
import os

qdrant_client = QdrantClient(url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Sabi works well"}

import traceback

@app.post("/voice_chat")
async def voice_chat(request: Request):
    try:
        data = await request.json()
        query = data.get("query")  # Extract the query from the request body

        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        # 💡 Add print to debug input
        print(f"🔍 Incoming query: {query}")

        # Get response from Gemini
        sabi_reply = gemini_response(query)

        print(f"✅ Gemini response: {sabi_reply}")

        return {"response": sabi_reply}

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()  # Logs the full traceback in your Railway logs
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
