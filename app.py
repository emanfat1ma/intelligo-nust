import os
import json
import logging
import asyncio
import chromadb
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import config
import llm  # Ensure llm.py has start_server() and kill_server()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nust-bot")

# --- LIFESPAN MANAGER (Modern FastAPI way) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run llama-server
    logger.info("⚙️ Starting llama-server...")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, llm.start_server)
    
    yield  # App runs here
    
    # Shutdown: Clean up
    logger.info("🛑 Killing llama-server...")
    llm.kill_server()

# Initialize App with lifespan
app = FastAPI(lifespan=lifespan)

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path=str(config.DB_DIR))
collection = chroma_client.get_or_create_collection(name="nust_docs")

# Serve static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    template_path = os.path.join("templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path) as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h2>Template index.html not found in /templates</h2>")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            user_msg = json.loads(data).get("message", "").strip()

            # 1. RAG Retrieval
            results = collection.query(query_texts=[user_msg], n_results=2)
            context = "\n---\n".join(results.get('documents', [[]])[0])

            # 2. Call the New Non-Streaming Function
            messages = [
                {"role": "system", "content": f"Answer ONLY using this context: {context} Keep it under 60 words."},
                {"role": "user", "content": user_msg}
            ]
            recent_messages = messages[-5:]
            # This is where the "wait" happens
            answer = await llm.get_chat_response(recent_messages)

            # 3. Send one single JSON back
            await websocket.send_json({"type": "full_text", "content": answer})

    except WebSocketDisconnect:
        logger.info("Client left.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)