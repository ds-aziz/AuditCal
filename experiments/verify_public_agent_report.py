"""Verify publicly released AI-agent report bytes against upstream LFS SHA256.

This is source integrity and exploratory extraction, NOT statistical validation.
Never execute AI-generated code from a downloaded source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from experiments.ingest_published_agent_reports import inspect_report

EXPECTED_SHA256 = "232c188e9aa155dee0056d79e115e065b85590b67be3972bb1dcae39dca2af23"
EXPECTED_BYTES = 16521
SOURCE_URL = (
    "https://github.com/amazon-science/agentic-forking-path/blob/main/"
    "experiment_data/workspaces/standard/"
    "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/"
    "sample_metr/2025-11-12T17-17-32%2B0000/mirrored_report.txt"
)

def validate(path: Path, source_root: Path) -> dict:
    b = path.read_bytes()
    actual_sha = hashlib.sha256(b).hexdigest()
    actual_size = len(b)
    source_match = actual_sha == EXPECTED_SHA256 and actual_size == EXPECTED_BYTES
    result = {
        "source": SOURCE_URL,
        "source_release": "amazon-science/agentic-forking-path",
        "reported_model": "Claude Sonnet 4.5 (inferred from path)",
        "reported_persona": "standard (inferred from path)",
        "reported_dataset": "sample_metr (inferred from path)",
        "actual_sha256": actual_sha,
        "expected_lfs_sha256": EXPECTED_SHA256,
        "actual_bytes": actual_size,
        "expected_bytes": EXPECTED_BYTES,
        "upstream_lfs_object_verified": source_match,
        "real_agent_report_available": False,
        "audited_statistical_claims": 0,
    }
    if not source_match:
        result["status"] = "SOURCE_INTEGRITY_FAILED_OR_POINTER_ONLY"
        return result
    row = inspect_report(path, source_root)
    result["status"] = row["status"]
    result["real_agent_report_available"] = row["status"] == "TEXT_AVAILABLE_NOT_AUTHENTICATED"
    result["unverified_statistical_mentions"] = len(row["candidates"])
    result["p_value_mentions"] = sum(c["kind"] == "p_value" for c in row["candidates"])
    result["coefficient_mentions"] = sum(c["kind"] == "coefficient" for c in row["candidates"])
    # Note: no model reconstruction, numeric truth assignment, or human labels exist yet.
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("source_root", type=Path)
    parser.add_argument("--out", type=Path, default=Path("results/one_verified_public_report.json"))
    args = parser.parse_args()
    report = validate(args.report, args.source_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["upstream_lfs_object_verified"] or not report["real_agent_report_available"]:
        raise SystemExit("Did not obtain original authenticated LFS report; stop without evaluation")

if __name__ == "__main__":
    main()
