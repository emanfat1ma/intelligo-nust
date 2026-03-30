import json
import logging
import os
import chromadb
import config
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _chunk_text(text, chunk_size=config.CHUNK_SIZE_WORDS, overlap=config.CHUNK_OVERLAP_WORDS):
    words = text.split()
    if len(words) <= chunk_size: return [text]
    chunks = []
    # Fixed chunking logic to prevent infinite loops
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_all_chunks():
    ids, texts, metadatas = [], [], []
    data_dir = config.DATA_DIR

    # 1. Process nust_faqs.json (List of Q&A)
    faq_path = data_dir / "nust_faqs.json"
    if faq_path.exists():
        logger.info("📦 Loading FAQs")
        faqs = _load_json(faq_path)
        for i, faq in enumerate(faqs):
            text = f"Question: {faq.get('question')}\nAnswer: {faq.get('answer')}"
            ids.append(f"faq_{i}")
            texts.append(text)
            metadatas.append({"source": "faq"})

    # 2. Process dates.json (List of Event Objects)
    dates_path = data_dir / "dates.json"
    if dates_path.exists():
        logger.info("📦 Loading Dates & Deadlines")
        dates_data = _load_json(dates_path)
        for entry in dates_data:
            text = f"Event: {entry.get('event')} | Date: {entry.get('date')} | Category: {entry.get('category')}"
            ids.append(f"date_{entry.get('id')}")
            texts.append(text)
            metadatas.append({"source": "dates", "category": entry.get("category")})

    # 3. Process acronym.json (Simple Dictionary)
    acronym_path = data_dir / "acronym.json"
    if acronym_path.exists():
        logger.info("📦 Loading Acronyms")
        acronyms = _load_json(acronym_path)
        # We group acronyms so the model sees multiple at once
        lines = [f"{k}: {v}" for k, v in acronyms.items()]
        for i in range(0, len(lines), 15): # Groups of 15
            group_text = "NUST Abbreviations and Terms:\n" + "\n".join(lines[i:i+15])
            ids.append(f"acronym_group_{i}")
            texts.append(group_text)
            metadatas.append({"source": "acronyms"})

    # 4. Process data.json (Nested Dictionary)
    # This file contains the 'university_identity' and 'detailed_institutions'
    data_path = data_dir / "data.json"
    if data_path.exists():
        logger.info("📦 Loading University Identity Data")
        univ_data = _load_json(data_path)
        # Convert the complex dictionary into a readable string format
        readable_content = json.dumps(univ_data, indent=2)
        for i, chunk in enumerate(_chunk_text(readable_content)):
            ids.append(f"univ_info_{i}")
            texts.append(chunk)
            metadatas.append({"source": "university_info"})

    return ids, texts, metadatas

if __name__ == "__main__":
    # Initialize Chroma
    client = chromadb.PersistentClient(path=str(config.DB_DIR))
    
    # Wipe old collection for a clean 2026 build
    try:
        client.delete_collection("nust_docs")
        logger.info("🗑️ Existing collection cleared.")
    except:
        pass
        
    collection = client.get_or_create_collection("nust_docs")
    
    # Load and Add
    i, t, m = load_all_chunks()
    
    if i:
        collection.add(ids=i, documents=t, metadatas=m)
        print(f"\n✅ Success! {len(i)} chunks from your JSON files are now indexed.")
    else:
        print("\n❌ Error: No data was loaded. Check your file names in the 'data' folder.")