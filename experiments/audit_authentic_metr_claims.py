"""Audit eight manually mapped structured claims from a REAL released agent report.

The structured claims below were transcribed by a researcher from the public
agent report and are NOT automatically extracted by AuditCal. Both source
report and comparison dataset have recorded provenance. Findings pertain ONLY
to the specified matched analyses; do not generalize benchmark performance.
"""
from __future__ import annotations
import json
from pathlib import Path
from auditcal import audit, SUPPORTED

REAL_REPORT_SHA256 = "232c188e9aa155dee0056d79e115e065b85590b67be3972bb1dcae39dca2af23"
REPORT_SOURCE = (
    "https://github.com/amazon-science/agentic-forking-path/blob/main/"
    "experiment_data/workspaces/standard/"
    "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/"
    "sample_metr/2025-11-12T17-17-32%2B0000/mirrored_report.txt"
)
MODEL_IDS = {
    "primary": "METR:log_initial_time~treatment+log_task_size:mixed_random_intercept_REML:N246",
    "secondary": "METR:log_total_time~treatment+log_task_size:cluster_robust_OLS:N230"
}
# These numbers were manually transcribed from a genuine AI-written report,
# separately retrieved and hash-verified against Amazon Science's Git LFS.
REPORTED = {
    "primary": {"p_value": 0.0658, "sample_size": 246,
                "significant": False, "pct_ci": [-0.95, 35.15]},
    "secondary": {"p_value": 0.0382, "sample_size": 230,
                  "significant": True, "pct_ci": [1.15, 42.64]}
}

def evaluate_released_report(reanalysis: dict) -> dict:
    records = []
    for category in ("primary", "secondary"):
        source_claims = REPORTED[category]
        evidence = reanalysis[category]["recomputed"]
        model_id = MODEL_IDS[category]
        provenance = {
            "source": REPORT_SOURCE,
            "verified_report_sha256": REAL_REPORT_SHA256,
            "original_dataset_sha256": reanalysis["dataset_sha256_downloaded_bytes"],
            "mapping": "Human-transcribed reported claims with original publication source",
            "independent_recomputation": reanalysis["evidence_provenance"]["github_actions_workflow_url"]
        }
        items = [
            ("p_value", source_claims["p_value"], evidence["p_value"], 0.0001),
            ("sample_size", source_claims["sample_size"], evidence["n"], 0),
            ("significant", source_claims["significant"], evidence["p_value"], None),
            ("confidence_interval", source_claims["pct_ci"], evidence["pct_ci"], 0.01),
        ]
        for kind, claimed, verified, tolerance in items:
            one = {
                "claim_id": f"genuine_agent_{category}_{kind}",
                "claim_type": kind,
                "reported": claimed,
                "verified": verified,
                "model_id": model_id,
                "evidence_model_id": model_id,
                "provenance": provenance,
            }
            if tolerance is not None:
                one["tolerance"] = tolerance
            result = audit(one)
            records.append({
                "claim_id": one["claim_id"],
                "claim_type": kind,
                "reported": claimed,
                "recomputed": verified,
                "tolerance": tolerance,
                **result.to_dict(),
            })
    summary = {
        "real_ai_agent_reports_with_hash_verified_text": 1,
        "agent_written_python_scripts_executed": 0,
        "source_dataset_used": reanalysis["source_dataset"],
        "report_source": REPORT_SOURCE,
        "report_source_sha256": REAL_REPORT_SHA256,
        "total_manually_transcribed_numerical_claims": len(records),
        "supported_under_matched_model": sum(x["status"] == SUPPORTED for x in records),
        "flagged_discrepancies": sum(x["status"] == "FLAGGED_DISCREPANCY" for x in records),
        "unverifiable": sum(x["status"] == "UNVERIFIABLE" for x in records),
        "independently_annotated_reports": 0,
        "independent_test_set_sample_size": 0,
        "scientific_novelty_proven": False,
        "note": (
            "Claim extraction and model match were manually specified. Agreement with "
            "published numerical results does not certify research design, causal "
            "validity, representativeness, or superiority of AuditCal."
        ),
    }
    return {"summary": summary, "claims": records}

def main():
    inp = Path("results/metr_independent_reanalysis_verified.json")
    source = json.loads(inp.read_text(encoding="utf-8"))
    assert source["evidence_provenance"]["github_actions_outcome"] == "success"
    out = evaluate_released_report(source)
    dest = Path("results/authentic_metr_claim_audit.json")
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out["summary"], indent=2))
    for x in out["claims"]:
        print(f"{x['claim_id']}: {x['status']}")
    if out["summary"]["supported_under_matched_model"] != 8:
        raise SystemExit("Unexpected discrepancy in one or more authentically reported numbers")

if __name__ == "__main__":
    main()
