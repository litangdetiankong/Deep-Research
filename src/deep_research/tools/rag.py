
from __future__ import annotations

from datetime import datetime,timezone
from pathlib import Path

import chromadb

from deep_research.schemas import Evidence


ROOT_DIR=Path(__file__).resolve().parents[3]
KB_DIR=ROOT_DIR / "knowledge_base" / "chroma"
COLLECTION_NAME="tech_research"

def get_collection():
    client=chromadb.PersistentClient(path=str(KB_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME)

def vector_search(query:str,top_k:int=4)->list[Evidence]:
    if not query.strip():
        return []

    collection=get_collection()

    result=collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents","metadatas","distances"],
    )

    documents=result["documents"][0] if result["documents"] else []
    metadatas=result["metadatas"][0] if result["metadatas"] else []
    distances=result["distances"][0] if result["distances"] else []
    ids=result["ids"][0] if result["ids"] else []

    evidence_list:list[Evidence]=[]
    now=datetime.now(timezone.utc).isoformat()

    for i,doc_text in enumerate(documents):
        meta=metadatas[i] if i<len(metadatas) else {}
        dist=distances[i] if i<len(distances) else None

        #distance越小通常越相似;先转成一个简单score
        score=0.0 if dist is None else 1.0/(1.0+float(dist))

        evidence_list.append(
            Evidence(
                id=ids[i] if i<len(ids) else f"ev_{i}",
                source=str(meta.get("source","")),
                title=str(meta.get("title","")),
                snippet=doc_text or "",
                retrieved_at=now,
                score=float(score),
            )
        )
    return evidence_list
