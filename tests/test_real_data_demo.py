"""Integration checks using the publicly bundled real US macro dataset."""
from experiments.real_data_validation import build_demo_claims, evaluate

def test_dataset_observations_and_provenance():
    records, metadata = build_demo_claims()
    assert metadata["n_observations"] == 203
    assert metadata["dataset"] == "statsmodels.datasets.macrodata"
    assert len(metadata["source_hash_selected_columns"]) == 64
    assert len(records) == 15
    assert metadata["genuine_ai_agent_traces"] == 0

def test_recomputed_evidence_not_hardcoded():
    records, _ = build_demo_claims()
    claim = next(rec for _, rec in records if rec["claim_id"] == "R2")
    assert claim["verified"] < 0
    assert claim["reported"] > 0

def test_expected_demo_results():
    rows, summary = evaluate()
    assert summary["self_authored_checks_matching"] == 15
    assert summary["expected_counts"] == {"supported": 6, "incorrect": 6, "unverifiable": 3}
    assert summary["real_ai_traces_evaluated"] == 0
    assert all(r["match"] for r in rows)
