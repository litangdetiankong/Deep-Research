from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_research.pipeline_m1 import run_plan_and_search
from deep_research.agents.critic import apply_critic_loop, run_critic
from deep_research.agents.writer import find_citations

ROOT = Path(__file__).resolve().parents[3]
QUESTIONS = ROOT / "data" / "eval" / "questions.jsonl"
OUT_DIR = ROOT / "outputs" / "eval"

REQUIRED_HEADERS = ["结论摘要", "分节论证", "不确定与局限", "参考来源"]

def eval_one(item: dict, max_rounds: int = 1) -> dict:
    q = item["question"]
    t0 = time.time()

    state = run_plan_and_search(q)
    state = apply_critic_loop(state, max_rounds=max_rounds)
    critic = run_critic(state)

    report = state.report_md or ""
    cites = find_citations(report)
    valid_ids = {e.id for e in state.evidence}
    unknown = [c for c in cites if c not in valid_ids]

    # 只把像 evidence id 的引用算进去，减少误伤
    id_like = [c for c in cites if "::" in c]
    unknown_id_like = [c for c in id_like if c not in valid_ids]

    missing_headers = [h for h in REQUIRED_HEADERS if h not in report]
    hit_keywords = [k for k in item.get("must_have_any", []) if k in report]

    latency = time.time() - t0
    return {
        "id": item.get("id"),
        "question": q,
        "latency_s": round(latency, 2),
        "evidence_count": len(state.evidence),
        "min_evidence_ok": len(state.evidence) >= int(item.get("min_evidence", 0)),
        "citation_count": len(id_like),
        "unknown_citation_count": len(unknown_id_like),
        "unknown_citations": unknown_id_like,
        "missing_headers": missing_headers,
        "keyword_hits": hit_keywords,
        "keyword_ok": len(hit_keywords) > 0 if item.get("must_have_any") else True,
        "critic_passed": critic.passed,
        "retry_count": state.metrics.retry_count,
        "research_id": state.research_id,
    }

def load_questions(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_report(results: list[dict], out_path: Path) -> None:
    n = len(results) or 1
    avg_latency = sum(r["latency_s"] for r in results) / n
    pass_rate = sum(1 for r in results if r["critic_passed"]) / n
    unk_rate = sum(r["unknown_citation_count"] for r in results) / max(sum(r["citation_count"] for r in results), 1)

    lines = [
        "# Eval Report",
        "",
        f"- cases: {len(results)}",
        f"- critic_pass_rate: {pass_rate:.2%}",
        f"- avg_latency_s: {avg_latency:.2f}",
        f"- unknown_id_citation_rate: {unk_rate:.2%}",
        "",
        "## Details",
        "",
    ]
    for r in results:
        lines.append(f"### {r['id']}")
        lines.append(f"- question: {r['question']}")
        lines.append(f"- latency_s: {r['latency_s']}")
        lines.append(f"- evidence_count: {r['evidence_count']} (min_ok={r['min_evidence_ok']})")
        lines.append(f"- citations: {r['citation_count']}, unknown: {r['unknown_citation_count']}")
        lines.append(f"- critic_passed: {r['critic_passed']}, retry: {r['retry_count']}")
        lines.append(f"- missing_headers: {r['missing_headers']}")
        lines.append(f"- keyword_hits: {r['keyword_hits']} (ok={r['keyword_ok']})")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    questions = load_questions(QUESTIONS)
    results = []
    for item in questions:
        print(f"running {item.get('id')} ...")
        results.append(eval_one(item, max_rounds=1))  # 评测可先 rounds=1 省钱

    out_json = OUT_DIR / "eval_results.json"
    out_md = OUT_DIR / "eval_report.md"
    out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(results, out_md)
    print("saved:", out_md)


if __name__ == "__main__":
    main()