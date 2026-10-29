"""Recompute evidence from public US macrodata. All reported claims are HUMAN-AUTHORED."""
import hashlib
import json
from collections import Counter
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN

DATASET = "statsmodels.datasets.macrodata"
MODEL_A = "macrodata:realcons~realdpi+unemp:ols:HC3"
MODEL_B = "macrodata:realcons~realdpi:ols:HC3"

def _source_and_models():
    frame = sm.datasets.macrodata.load_pandas().data
    canonical = frame[["realcons", "realdpi", "unemp"]].to_csv(index=False, float_format="%.15g").encode("utf-8")
    sha = hashlib.sha256(canonical).hexdigest()
    a = smf.ols("realcons ~ realdpi + unemp", data=frame).fit(cov_type="HC3")
    b = smf.ols("realcons ~ realdpi", data=frame).fit(cov_type="HC3")
    return sha, a, b

def _base(claim_id, kind, reported, verified, model_id, evidence_model_id, sha, **kwargs):
    return dict(
        claim_id=claim_id, claim_type=kind, reported=reported, verified=verified,
        model_id=model_id, evidence_model_id=evidence_model_id,
        provenance={"source": DATASET, "sha256_selected_columns": sha,
                    "calculation": "statsmodels OLS fit(cov_type='HC3')"}, **kwargs)

def build_demo_claims():
    sha, a, b = _source_and_models()
    coef = float(a.params["unemp"])
    p = float(a.pvalues["unemp"])
    ci = list(map(float, a.conf_int().loc["unemp"].tolist()))
    b_coef = float(b.params["realdpi"])
    records = [
        ("supported", _base("R1", "coefficient", coef, coef, MODEL_A, MODEL_A, sha)),
        ("incorrect", _base("R2", "coefficient", abs(coef), coef, MODEL_A, MODEL_A, sha)),
        ("supported", _base("R3", "p_value", p, p, MODEL_A, MODEL_A, sha)),
        ("incorrect", _base("R4", "p_value", 0.7, p, MODEL_A, MODEL_A, sha)),
        ("supported", _base("R5", "confidence_interval", ci, ci, MODEL_A, MODEL_A, sha)),
        ("incorrect", _base("R6", "confidence_interval", [-10.0,-5.0], ci, MODEL_A, MODEL_A, sha)),
        ("supported", _base("R7", "sample_size", int(a.nobs), int(a.nobs), MODEL_A, MODEL_A, sha)),
        ("incorrect", _base("R8", "sample_size", 100, int(a.nobs), MODEL_A, MODEL_A, sha)),
        ("supported", _base("R9", "sign", "negative", coef, MODEL_A, MODEL_A, sha)),
        ("incorrect", _base("R10", "sign", "positive", coef, MODEL_A, MODEL_A, sha)),
        ("supported", _base("R11", "significant", True, p, MODEL_A, MODEL_A, sha, alpha=0.05)),
        ("incorrect", _base("R12", "significant", False, p, MODEL_A, MODEL_A, sha, alpha=0.05)),
        ("unverifiable", _base("R13", "coefficient", b_coef, coef, MODEL_B, MODEL_A, sha)),
        ("unverifiable", _base("R14", "causal", True, True, MODEL_A, MODEL_A, sha)),
        ("unverifiable", _base("R15", "p_value", 0.1, None, MODEL_A, MODEL_A, sha)),
    ]
    metadata = {"dataset": DATASET, "source_hash_selected_columns": sha,
                "n_observations": int(a.nobs), "model_a": MODEL_A, "model_b": MODEL_B,
                "outcomes_are_human_authored": True, "genuine_ai_agent_traces": 0,
                "statsmodels_version": sm.__version__, "pandas_version": pd.__version__}
    return records, metadata

def evaluate():
    records, metadata = build_demo_claims()
    mapping = {"supported": SUPPORTED, "incorrect": FLAGGED, "unverifiable": ABSTAIN}
    rows = []
    for expected, claim in records:
        got = audit(claim)
        rows.append({"claim_id": claim["claim_id"], "hand_authored_expected": expected,
                     "expected_status": mapping[expected], "actual_status": got.status,
                     "match": got.status == mapping[expected], "reason": got.reason})
    summary = {"metadata": metadata, "n_hand_authored_cases": len(rows),
               "expected_counts": dict(Counter(x["hand_authored_expected"] for x in rows)),
               "status_counts": dict(Counter(x["actual_status"] for x in rows)),
               "self_authored_checks_matching": sum(x["match"] for x in rows),
               "self_authored_checks_total": len(rows), "real_ai_traces_evaluated": 0,
               "interpretation": "Engineering reproducibility demonstration, not independent performance evaluation"}
    return rows, summary

def main():
    rows, summary = evaluate()
    target = Path(__file__).resolve().parents[1] / "results"
    target.mkdir(exist_ok=True)
    (target / "macrodata_ols_hc3_rows.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    (target / "macrodata_ols_hc3_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if summary["self_authored_checks_matching"] != summary["self_authored_checks_total"]:
        raise SystemExit("An authored expectation did not match; inspect results")

if __name__ == "__main__":
    main()
