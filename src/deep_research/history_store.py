from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent
ROOT = Path(__file__).resolve().parents[2]  # 先 print 验证：应指向 Deep-Research 或 src 的上一级

ROOT_DIR = Path(__file__).resolve().parents[2]
HISTORY_DIR = ROOT_DIR / "outputs" / "history"
HISTORY_FILE = HISTORY_DIR / "history.jsonl"


def _ensure():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("", encoding="utf-8")


def append_history(item: dict) -> None:
    _ensure()
    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def list_history(limit: int = 50) -> list[dict]:
    _ensure()
    rows: list[dict] = []
    text = HISTORY_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    rows.reverse()  # 最新在前
    return rows[:limit]


def get_history(research_id: str) -> dict | None:
    for item in list_history(limit=10000):
        if item.get("research_id") == research_id:
            return item
    return None