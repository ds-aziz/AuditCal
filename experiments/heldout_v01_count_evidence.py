"""Independent source-only counts for the frozen held-out v0.1 claim selection.

This does NOT adjudicate model-dependent claims, calculate p-values, or assert a
double-reviewed gold label. All inputs are hash-locked public research data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "evaluation/heldout_v01_selected_claims.json"
METR_SHA = "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
SOCCER_SHA = "6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"


def read_dataset(path: Path, expected_sha: str, key: str) -> dict:
    with path.open("rb") as f:
        sha = hashlib.file_digest(f, "sha256").hexdigest()
    if sha != expected_sha:
        raise ValueError(f"{path.name}: source hash mismatch {sha} != {expected_sha}")
    rows = 0
    groups = set()
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if key not in (reader.fieldnames or []):
            raise ValueError(f"{path.name}: missing expected {key!r} identifier")
        for row in reader:
            rows += 1
            if row[key] not in ("", None):
                groups.add(row[key])
    return {"sha256": sha, "rows": rows, "distinct_entity_count": len(groups),
            "entity_column": key,
            "group_values": sorted(groups) if key == "leagueCountry" else None}


def run(metr: Path, soccer: Path) -> dict:
    claims = json.loads(CLAIMS.read_text(encoding="utf-8"))
    expected_ids = {"S1-C1", "S1-C2", "S2-C1", "S2-C2", "S4-C1", "S4-C2"}
    assert len(claims["claims"]) == 24
    by_id = {c["claim_id"]: c for c in claims["claims"]}
    assert all(i in by_id for i in expected_ids)
    m = read_dataset(metr, METR_SHA, "dev_id")
    s = read_dataset(soccer, SOCCER_SHA, "leagueCountry")
    evidence = {
        "S1-C1": (m["distinct_entity_count"], "METR entire primary source developers"),
        "S1-C2": (m["rows"], "METR entire source dataset tasks"),
        "S2-C1": (m["rows"], "METR entire source dataset tasks"),
        "S2-C2": (m["distinct_entity_count"], "METR entire primary source developers"),
        "S4-C1": (s["rows"], "Soccer educational public source copy, unfiltered dyads"),
        "S4-C2": (s["distinct_entity_count"], "Soccer educational copy, distinct raw leagueCountry values"),
    }
    rows = []
    for cid, (recomputed, sample_identity) in evidence.items():
        c = by_id[cid]
        if c["claim_type"] not in ("sample_size", "distinct_count"):
            raise ValueError(f"Unexpected noncount selected claim {cid}")
        rows.append({
            "claim_id": cid,
            "reported": c["reported"],
            "recomputed_raw_source": recomputed,
            "same_source_context_verified": True,
            "sample_identity": sample_identity,
            "preliminary_count_agreement": int(c["reported"]) == int(recomputed),
            "human_second_review": False,
            "gold_label": None,
            "interpretation": "SINGLE_RESEARCHER_SOURCE_COUNT_CHECK_ONLY"
        })
    return {
        "scope": "Six pre-frozen raw-source count claims only; other 18 selected claims NOT tested",
        "source_data": {"METR": m, "Soccer_educational_copy": s},
        "rows": rows,
        "source_count_claims_checked": len(rows),
        "count_agreements": sum(x["preliminary_count_agreement"] for x in rows),
        "unreviewed_selected_claims": 24 - len(rows),
        "scientific_accuracy_rate_claimed": False,
        "independent_gold_review_completed": False,
        "source_agent_code_executed": False,
        "note": "This is a bounded source-count feasibility check, not a final held-out reliability benchmark. "
                "Some samples in other reports are filtered and cannot be checked against raw-row counts."
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--metr", required=True, type=Path)
    p.add_argument("--soccer", required=True, type=Path)
    p.add_argument("--output", default="results/heldout_v01/raw_source_count_evidence.json", type=Path)
    x = p.parse_args()
    result = run(x.metr, x.soccer)
    x.output.parent.mkdir(parents=True, exist_ok=True)
    x.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("FROZEN_SOURCE_COUNT_READOUT", json.dumps({
        "source_count_claims_checked": result["source_count_claims_checked"],
        "count_agreements": result["count_agreements"],
        "unreviewed_selected_claims": result["unreviewed_selected_claims"],
        "source_data": result["source_data"],
        "rows": result["rows"]
    }), flush=True)
    if result["count_agreements"] != result["source_count_claims_checked"]:
        raise SystemExit("At least one count differs; do not silently accept.")


if __name__ == "__main__":
    main()
