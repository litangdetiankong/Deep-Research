from __future__ import annotations

from pathlib import Path
import re

import chromadb

#本文件在scripts/下，parents[1]就是项目根D:\Deep-Research
ROOT_DIR=Path(__file__).resolve().parents[1]
RAW_DIR=ROOT_DIR / "data" / "raw"
KB_DIR=ROOT_DIR / "knowledge_base" / "chroma"
COLLECTION_NAME="tech_research"

def read_raw_files()->list[dict]:
    files=sorted(list(RAW_DIR.glob("*.md"))+list(RAW_DIR.glob("*.txt")))
    docs=[]

    for path in files:
        text=path.read_text(encoding="utf-8")
        doc_id=path.stem

        title=doc_id
        for line in text.splitlines():
            if line.startswith("# "):
                title=line[2:].strip()
                break

        source=f"file://{path.as_posix()}"
        m=re.search(r"^source:\s*(.+)$",text,flags=re.MULTILINE)
        if m:
            source=m.group(1).strip()

        docs.append(
            {
                "path":str(path),
                "doc_id":doc_id,
                "title":title,
                "source":source,
                "text":text,
            }
        )

    return docs

def chunk_text(text:str,chunk_size:int=600,overlap:int=100)->list[str]:
    text=text.strip()
    if not text:
        return []

    if len(text)<=chunk_size:
        return [text]

    chunks:list[str]=[]
    start=0
    n=len(text)

    while start<n:
        end=min(start+chunk_size,n)
        piece=text[start:end].strip()
        if piece:
            chunks.append(piece)

        if end>=n:
            break

        #下一步起点:往回重叠overlap,避免边界语义被切断
        start=end-overlap
        if start<0:
            start=0
    return chunks

def build_chunk_records(docs:list[dict])->tuple[list[str],list[str],list[dict]]:
    ids:list[str]=[]
    documents:list[str]=[]
    metadatas:list[dict]=[]

    for doc in docs:
        pieces=chunk_text(doc["text"])
        for i,piece in enumerate(pieces):
            ids.append(f"{doc['doc_id']}::{i}")
            documents.append(piece)
            metadatas.append({
                "doc_id":doc["doc_id"],
                "title":doc["title"],
                "source":doc["source"],
                "chunk_index":i,
            })
    return ids,documents,metadatas

def ingest()->int:
    docs=read_raw_files()
    if not docs:
        raise FileNotFoundError(f"未找到文档:{RAW_DIR}")

    ids,documents,metadatas=build_chunk_records(docs)

    KB_DIR.mkdir(parents=True,exist_ok=True)

    client=chromadb.PersistentClient(path=str(KB_DIR))

    #学习阶段:每次重建,避免重复累加
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection=client.get_or_create_collection(name=COLLECTION_NAME)

    #可分批add;文档少时一次写入即可
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    count=collection.count()
    print(f"files={len(docs)},chunks_written={len(ids)},collection_count={count}")
    print(f"kb_path={KB_DIR}")
    return count

if __name__ == "__main__":
    ingest()
