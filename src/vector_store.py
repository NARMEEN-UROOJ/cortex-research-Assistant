import chromadb
from chromadb.utils import embedding_functions
import os
from pathlib import Path
import importlib

PdfReader = None
for _module_name in ("pypdf", "PyPDF2"):
    try:
        _module = importlib.import_module(_module_name)
        PdfReader = getattr(_module, "PdfReader", None)
        if PdfReader is not None:
            break
    except Exception:
        continue

# ── Setup ChromaDB ────────────────────────────────────────────────────────────
def get_client():
    """Returns a persistent ChromaDB client."""
    os.makedirs("vector_db", exist_ok=True)
    return chromadb.PersistentClient(path="vector_db")

def get_collection(name: str = "research_docs"):
    """Gets or creates a collection with sentence-transformers embeddings."""
    client = get_client()
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_fn
    )

# ── Document Processing ───────────────────────────────────────────────────────
def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        if PdfReader is None:
            return "Error reading PDF: Missing dependency. Install 'pypdf' (recommended) or 'PyPDF2'."

        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_txt(file_path: str) -> str:
    """Extracts text from a TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits text into overlapping chunks for better retrieval.
    overlap ensures context isn't lost at chunk boundaries.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

# ── Add Documents ─────────────────────────────────────────────────────────────
def add_document(file_path: str, doc_name: str) -> dict:
    """
    Processes a document and adds it to ChromaDB.
    Returns a summary of what was added.
    """
    ext = Path(file_path).suffix.lower()

    # Extract text
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        return {"success": False, "error": f"Unsupported file type: {ext}"}

    if not text or text.startswith("Error"):
        return {"success": False, "error": text}

    # Chunk the text
    chunks = chunk_text(text)
    if not chunks:
        return {"success": False, "error": "No text could be extracted"}

    # Add to ChromaDB
    collection = get_collection()
    ids       = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_name, "chunk": i} for i in range(len(chunks))]

    # Remove existing chunks for this doc if re-uploading
    try:
        existing = collection.get(where={"source": doc_name})
        if existing["ids"]:
            collection.delete(where={"source": doc_name})
    except Exception:
        pass

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )

    return {
        "success": True,
        "doc_name": doc_name,
        "chunks": len(chunks),
        "chars": len(text)
    }

# ── Query Documents ───────────────────────────────────────────────────────────
def query_documents(query: str, n_results: int = 5) -> str:
    """
    Searches ChromaDB for chunks relevant to the query.
    Returns formatted results the agents can read.
    """
    try:
        collection = get_collection()
        count = collection.count()
        if count == 0:
            return ""

        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )

        if not results["documents"] or not results["documents"][0]:
            return ""

        formatted = "\n\n--- Relevant content from your documents ---\n"
        for i, (doc, meta) in enumerate(
            zip(results["documents"][0], results["metadatas"][0])
        ):
            formatted += f"\n[From: {meta['source']}]\n{doc}\n"

        return formatted

    except Exception as e:
        return f"Document search error: {str(e)}"

# ── List & Delete Documents ───────────────────────────────────────────────────
def list_documents() -> list:
    """Returns a list of all unique document names in the collection."""
    try:
        collection = get_collection()
        if collection.count() == 0:
            return []
        results = collection.get()
        sources = list(set(m["source"] for m in results["metadatas"]))
        return sorted(sources)
    except Exception:
        return []

def delete_document(doc_name: str) -> bool:
    """Deletes all chunks of a document from ChromaDB."""
    try:
        collection = get_collection()
        collection.delete(where={"source": doc_name})
        return True
    except Exception:
        return False

def get_document_count() -> int:
    """Returns total number of chunks stored."""
    try:
        return get_collection().count()
    except Exception:
        return 0