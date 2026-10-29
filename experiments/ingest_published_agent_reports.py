"""Read published AI-agent reports without executing untrusted code.

A report's model/persona attribution is only inferred from path.
Numbers extracted from prose are UNVERIFIED candidates, not scored errors.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REPORT_NAME = "mirrored_report.txt"
LFS_HEADER = "version https://git-lfs.github.com/spec/v1"
REGEX_P = re.compile(r"(?i)\b(?:p[-\s]?value)\s*(?:[:=]|\bis\b)?\s*([<>]=?|=)?\s*(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)")
REGEX_COEF = re.compile(r"(?i)\b(?:coefficient|effect estimate)\s*(?:[:=]|\bis\b)\s*([-+]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)")

def file_identity(path: Path) -> dict[str, Any]:
    """Filename-based attribution does not authenticate the report."""
    parts = path.parts
    if "workspaces" not in parts:
        return {"attribution": "UNVERIFIED_PATH", "persona": None, "model": None, "dataset": None, "run_id": None}
    after = parts[parts.index("workspaces") + 1:]
    if len(after) < 5 or after[-1] != REPORT_NAME:
        return {"attribution": "UNVERIFIED_PATH", "persona": None, "model": None, "dataset": None, "run_id": None}
    return {"attribution": "PATH_INFERRED_NOT_AUTHENTICATED", "persona": after[0], "model": after[1], "dataset": after[2], "run_id": after[3]}

def extract_candidates(raw: str, source_id: str) -> list[dict[str, Any]]:
    """Extract literal mentions only; no scientific judgement or labels."""
    candidates: list[dict[str, Any]] = []
    for kind, regex in [("p_value", REGEX_P), ("coefficient", REGEX_COEF)]:
        for match in regex.finditer(raw):
            operator = (match.group(1) or "=") if kind == "p_value" else "="
            value = match.group(2) if kind == "p_value" else match.group(1)
            try:
                numeric = float(value)
            except ValueError:
                continue
            if kind == "p_value" and not (0 <= numeric <= 1):
                continue
            candidates.append({
                "candidate_id": f"{source_id}:{len(candidates)+1}",
                "kind": kind, "reported_number": numeric, "operator": operator,
                "validation_status": "REQUIRES_HUMAN_REVIEW",
                "scientific_evidence": None,
                "context": raw[max(0, match.start()-70):min(len(raw), match.end()+70)].replace("\n", " ")[:180]
            })
    return candidates

def inspect_report(path: Path, base: Path) -> dict[str, Any]:
    """Read text safely and reject Git LFS pointer masquerading as a report."""
    result: dict[str, Any] = {"path": path.relative_to(base).as_posix(), "record_kind": "SOURCE_TRIAGE"}
    result.update(file_identity(path))
    contents = path.read_bytes()
    result["sha256_local_bytes"] = hashlib.sha256(contents).hexdigest()
    result["byte_length_local"] = len(contents)
    try:
        raw = contents.decode("utf-8")
    except UnicodeDecodeError:
        result.update(status="UNREADABLE_TEXT", candidates=[])
        return result
    if raw.startswith(LFS_HEADER):
        oid = re.search(r"^oid sha256:([a-f0-9]{64})$", raw, re.M)
        size = re.search(r"^size (\d+)$", raw, re.M)
        result.update(
            status="LFS_POINTER_NOT_AGENT_TEXT",
            expected_lfs_sha256=oid.group(1) if oid else None,
            expected_lfs_bytes=int(size.group(1)) if size else None,
            candidates=[])
        return result
    if not raw.strip():
        result.update(status="EMPTY_TEXT", candidates=[])
        return result
    key = result["sha256_local_bytes"][:16]
    result.update(
        status="TEXT_AVAILABLE_NOT_AUTHENTICATED",
        candidates=extract_candidates(raw, key),
        note="Human review and model-matched numeric recomputation required before scoring")
    return result

def ingest(root: Path, limit: int | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    base = root.resolve()
    if not base.is_dir():
        raise ValueError(f"Not a directory: {root}")
    paths = sorted(base.rglob(REPORT_NAME))
    if limit is not None:
        if limit < 1:
            raise ValueError("--limit must be positive")
        paths = paths[:limit]
    rows = [inspect_report(p, base) for p in paths if p.is_file()]
    counts = Counter(r["status"] for r in rows)
    summary = {
        "total_report_paths_scanned": len(rows),
        "by_status": dict(sorted(counts.items())),
        "candidate_mentions_not_validated": sum(len(r["candidates"]) for r in rows),
        "confirmed_authenticated_AI_traces": 0,
        "independently_verified_AI_statistical_errors": 0,
        "meaning": "Source triage, not evaluation. Authenticity and gold labels require independent checks."
    }
    return rows, summary

def main() -> None:
    parser = argparse.ArgumentParser(description="Safe source triage for AI-agent reports")
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/published_report_triage.jsonl"))
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    rows, summary = ingest(args.root, args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
