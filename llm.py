import ollama
import asyncio
import config
import logging

logger = logging.getLogger(__name__)
def start_server():
    logger.info("Checking Ollama status... (Make sure the Ollama app is running!)")
    return None

def kill_server():
    pass

async def get_chat_response(messages):
    try:
        # 1. Use the AsyncClient
        client = ollama.AsyncClient() 
        
        # 2. Pass the 'messages' argument directly
        response = await client.chat(
            model='llama3.2:1b', 
            messages=messages,  # Use the list passed from app.py
            options={
                'temperature': 0.0,
                'num_predict': 80,
                'top_k': 1,
                'num_thread': 4 
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"