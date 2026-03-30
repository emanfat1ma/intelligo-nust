from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "db"

# LLM Server Settings
QWEN_GGUF = "models/qwen2.5-0.5b-instruct.gguf"  # Update to your actual model path
N_THREADS = 4
LLAMA_HOST = "127.0.0.1"
LLAMA_PORT = 8080
LLAMA_HEALTH_URL = f"http://{LLAMA_HOST}:{LLAMA_PORT}/health"
LLAMA_CHAT_URL = f"http://{LLAMA_HOST}:{LLAMA_PORT}/v1/chat/completions"

# RAG Settings
CHUNK_SIZE_WORDS = 300
CHUNK_OVERLAP_WORDS = 50

# Generation Settings
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 512