"""
DocBot: a deliberately vulnerable RAG chatbot for CycleShop internal docs.

Module 3 target (indirect injection). It loads a folder of policy documents
into ChromaDB, retrieves the most relevant chunks for each question, and
pastes them into the prompt. It cannot tell document text from instructions,
so a payload hidden in a document can hijack its answers.

DO NOT deploy. For local learning only.

Setup:
    cd 03-indirect
    source ../.venv/bin/activate
    uv pip install chromadb langchain langchain-community langchain-ollama pypdf
    python docbot.py ingest      # load docs/ into the vector store
    python docbot.py ask "what is the refund policy?"
    python docbot.py serve        # optional web UI on :8200
"""

import os
import sys
import glob
import pathlib

import requests
import chromadb
from chromadb.utils import embedding_functions

HERE = pathlib.Path(__file__).parent
DOCS_DIR = HERE / "docs"
DB_DIR = HERE / "chroma_store"

OLLAMA_URL = os.getenv("APP_OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL_NAME", "llama3.2:3b")

SYSTEM_PROMPT = """You are DocBot, an assistant for CycleShop staff.
Answer questions using ONLY the provided context documents.
Be concise. If the answer is not in the context, say you do not know.
"""


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    # Use a local sentence-transformer embedding so nothing leaves the machine.
    ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(name="cycleshop_docs", embedding_function=ef)


def chunk_text(text, size=500, overlap=50):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def ingest():
    """Load every .txt and .md file in docs/ into the vector store."""
    col = get_collection()
    # Clear old data so re-ingesting is clean.
    existing = col.get()
    if existing["ids"]:
        col.delete(ids=existing["ids"])

    ids, docs, metas = [], [], []
    files = glob.glob(str(DOCS_DIR / "*.txt")) + glob.glob(str(DOCS_DIR / "*.md"))
    for path in files:
        name = pathlib.Path(path).name
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{name}:{i}")
            docs.append(chunk)
            metas.append({"source": name})

    if not ids:
        print(f"No .txt or .md files found in {DOCS_DIR}. Add some first.")
        return
    col.add(ids=ids, documents=docs, metadatas=metas)
    print(f"Ingested {len(ids)} chunks from {len(files)} files.")


def retrieve(question, k=3):
    col = get_collection()
    res = col.query(query_texts=[question], n_results=k)
    chunks = res["documents"][0]
    sources = [m["source"] for m in res["metadatas"][0]]
    return chunks, sources


def ask_model(question, context):
    prompt = f"{SYSTEM_PROMPT}\n\nContext documents:\n{context}\n\nQuestion: {question}"
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]


def ask(question):
    chunks, sources = retrieve(question)
    context = "\n\n---\n\n".join(chunks)
    answer = ask_model(question, context)
    print("ANSWER:\n" + answer)
    print("\nRETRIEVED FROM:", ", ".join(sources))
    return answer


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "ingest":
        ingest()
    elif cmd == "ask":
        ask(" ".join(sys.argv[2:]) or "what is the refund policy?")
    else:
        print(__doc__)