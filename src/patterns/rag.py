import os
import glob
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from src.llm_client import OllamaClient

EMB = SentenceTransformer("all-MiniLM-L6-v2")  # small & fast

def build_or_load_collection(path: str = "data", name: str = "local_docs"):
    client = chromadb.Client()
    coll = client.get_or_create_collection(name)
    if coll.count() == 0:
        docs, ids, metas = [], [], []
        for fp in sorted(glob.glob(os.path.join(path, "**", "*.*"), recursive=True)):
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                docs.append(content)
                ids.append(fp)
                metas.append({"path": fp})
            except Exception:
                continue
        if docs:
            embs = EMB.encode(docs, convert_to_numpy=True).tolist()
            coll.add(documents=docs, embeddings=embs, ids=ids, metadatas=metas)
    return coll

def answer_with_rag(client: OllamaClient, question: str, k: int = 4) -> str:
    coll = build_or_load_collection()
    qemb = EMB.encode([question])[0].tolist()
    res = coll.query(query_embeddings=[qemb], n_results=k)
    docs: List[str] = res.get("documents", [[]])[0]
    metas: List[dict] = res.get("metadatas", [[]])[0]
    ctx = "\n\n---\n\n".join(docs)
    citation = ", ".join([m.get("path", "?") for m in metas])
    prompt = (
        "Use only the CONTEXT to answer. If insufficient, say so.\n\n"
        f"CONTEXT:\n{ctx}\n\n"
        f"QUESTION: {question}\n\nInclude cited files: {citation}"
    )
    return client.generate(prompt, system="Ground answers in the provided context; cite filenames when possible.")
