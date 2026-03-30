IntelliGo: Offline NUST Admission Assistant
IntelliGo is a high-performance, RAG-based (Retrieval-Augmented Generation) chatbot designed to provide instant, verified answers to NUST admission queries. It is specifically engineered to run 100% offline on consumer-grade hardware, ensuring data privacy and accessibility without a GPU.

🚀 Key Features
Source Grounding: Directly indexed from the official NUST FAQs.

Fully Offline: Utilizes Ollama and ChromaDB for local inference and vector storage.

Hardware Optimized: Runs smoothly on 8GB RAM and i5 CPUs using quantized Llama 3.2 (1B/3B) or Phi-3 models.

Zero-Hallucination: Strictly maps user intent to official university policies regarding merit lists, scholarships (NFAAF/NNBS), and hostels.

🛠️ Tech Stack
Backend: FastAPI (Python)

LLM Engine: Ollama (Llama 3.2 / Phi-3)

Vector Database: ChromaDB

Frontend: HTML5/CSS3 & JavaScript (WebSockets)

💻 Hardware Requirements
RAM: 8GB (Minimum)

CPU: Intel Core i5 (10th Gen or newer recommended)

GPU: Not required (CPU-only optimized)

OS: Windows / Linux / macOS

🔧 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/emanfat1ma/intelligo-nust.git
cd intelligo-nust
Set up a Virtual Environment:

Bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
Install & Pull the Model:
Download Ollama and run:

Bash
ollama pull llama3.2:1b
Run the Application:

Bash
python app.py
Access the interface at http://127.0.0.1:8000.

📂 Project Structure
app.py: FastAPI application & WebSocket logic.

ingest.py: Scripts for processing FAQ data into ChromaDB.

llm.py: Interaction logic with the local Ollama instance.

data/: Contains the nust_faqs.json source data.

.gitignore: Configured to exclude heavy model weights (.gguf) and local DBs.
