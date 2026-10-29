"""Stage 9 fixed evidence tests; NOT a held-out statistical benchmark.

6 genuine reports from 3 other AI models. All source claim transcription
and model alignment were researcher-specified, not independently blinded.
"""
import json
from pathlib import Path

from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN

EVIDENCE = (Path(__file__).resolve().parents[1] /
            "results/stage9_other_models_verified_numeric_snapshot.json")

def read_evidence():
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert data["dataset_sha256"] == "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
    assert data["execution"]["result"] == "success"
    assert data["original_agent_scripts_executed"] is False
    return data

def claim(reported, verified, reported_model, evidence_model, tolerance=0.003):
    return audit({
        "claim_id": "stage9_example",
        "claim_type": "p_value",
        "reported": reported, "verified": verified,
        "model_id": reported_model, "evidence_model_id": evidence_model,
        "provenance": {"source": "hash_verified_released_agent_report"},
        "tolerance": tolerance})

def test_all_six_approximate_source_mapped_primary_numbers_agree():
    data = read_evidence()
    assert data["report_count"] == 6
    assert data["distinct_models_tested"] == 3
    assert len(data["checks"]) == 6
    for item in data["checks"]:
        model = item["method_identity_researcher_mapped"]
        assert claim(item["original_report_p_value"],
                     data["models"][model]["p_value"],
                     model, model).status == SUPPORTED

def test_strict_decimal_rounding_is_five_of_six_not_six_of_six():
    data = read_evidence()
    # Digits actually displayed in selected public reports, in run order.
    published_places = (4, 3, 3, 3, 4, 4)
    clear = []
    review = []
    for item, places in zip(data["checks"], published_places):
        delta = abs(item["difference_p"])
        allowed = 0.5 * 10**(-places)
        (clear if delta <= allowed else review).append(item["run_id"])
    assert len(clear) == 5
    assert review == ["2025-11-14T15-33-39+0000"]

def test_haiku_difference_does_not_cross_significance_threshold():
    data = read_evidence()
    haiku = data["checks"][1]
    assert haiku["ai_model"] == "Claude Haiku 4.5"
    assert haiku["original_report_p_value"] > 0.05
    assert haiku["independently_recomputed"]["p_value"] > 0.05

def test_different_qwen_coder_specification_requires_abstention():
    data = read_evidence()
    reported = data["checks"][-1]["original_report_p_value"]
    canonical = data["models"]["standard"]["p_value"]
    output = claim(reported, canonical,
                   reported_model="coder_variant",
                   evidence_model="standard")
    assert output.status == ABSTAIN

def test_injected_wrong_value_is_separate_from_genuine_agent_reports():
    data = read_evidence()
    assert claim(0.7, data["models"]["standard"]["p_value"],
                 "standard", "standard").status == FLAGGED

def test_shifted_time_outcome_not_identical_to_plain_time_ratio():
    data = read_evidence()
    coder = data["models"]["coder_variant"]
    assert "log_initial_plus1" in coder["formula"]
    assert "average_predicted_time" in coder["formula"]
    assert abs(coder["p_value"] - 0.1158) < 0.00005
    assert abs(coder["gmr_from_transformed_outcome"] - 1.1392) < 0.00005
    assert "not" in data["methodological_note"].lower()
