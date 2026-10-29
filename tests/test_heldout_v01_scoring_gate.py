"""Software-only tests using MADE-UP fixtures.

These test control-flow and arithmetic. They do not constitute independent
reviewers, gold labels, research case studies, or a measured held-out benchmark.
"""
from copy import deepcopy
import pytest

from auditcal import audit, ABSTAIN, FLAGGED
from evaluation.heldout_v01_scoring_gate import (
    EvidenceGateBlocked, double_reviewed_labels, frozen_claims, ready_for_scoring, score
)


def fake_reviews_and_predictions():
    locked = frozen_claims()
    claims = [
        {"claim_id": cid, "source_report_sha256": row["source_report_sha256"],
         "gold_label": "SUPPORTED_GOLD", "independent_reanalysis_reference": "synthetic unit fixture",
         "source_method_reference": "made-up unit test evidence",
         "rationale": "software gate test only, not a real reviewer"}
        for cid, row in locked.items()
    ]
    def fake_reviewer(uid):
        return {
            "reviewer": {
                "reviewer_id": uid, "name": "SYNTHETIC TEST PERSON " + uid,
                "signed_date": "2026-01-01",
                "signed_attestation": "SYNTHETIC NOT A REAL SIGNATURE",
                "independent_human": True,
                "blind_to_system_predictions": True,
                "no_involvement_in_auditcal_development": True
            },
            "claims": deepcopy(claims)
        }
    one, two = fake_reviewer("unit-A"), fake_reviewer("unit-B")
    predictions = {
        "run_metadata": {
            "auditcal_code_commit": "synthetic",
            "baseline_code_commit": "synthetic",
            "source_evidence_manifest": "synthetic",
            "run_log_url": "synthetic unit test, not real run"
        },
        "auditcal": [
            {"claim_id": cid, "status": "SUPPORTED", "reason": "synthetic unit fixture"}
            for cid in locked
        ],
        "naive": [
            {"claim_id": cid, "status": "SUPPORTED", "reason": "synthetic unit fixture"}
            for cid in locked
        ]
    }
    return locked, one, two, predictions


def test_24_locked_claims_are_unique():
    locked = frozen_claims()
    assert len(locked) == 24
    assert set(locked) == {f"S{i}-C{j}" for i in range(1, 9) for j in range(1, 4)}


def test_synthetic_fixtures_only_score_after_complete_attested_input():
    locked, a, b, p = fake_reviews_and_predictions()
    res = ready_for_scoring(locked, a, b, p)
    assert res["claims_selected"] == 24
    assert res["auditcal"]["coverage_all"]["numerator"] == 24
    assert res["auditcal"]["false_flag_rate_on_supported"]["numerator"] == 0
    assert res["auditcal"]["error_recall_abstain_counts_as_miss"]["rate"] is None
    assert res["auditcal"]["confusion_3x3"]["SUPPORTED_GOLD"]["SUPPORTED"] == 24


def test_reject_nonindependent_same_reviewer():
    locked, a, b, p = fake_reviews_and_predictions()
    b["reviewer"]["reviewer_id"] = a["reviewer"]["reviewer_id"]
    with pytest.raises(EvidenceGateBlocked, match="distinct identities"):
        ready_for_scoring(locked, a, b, p)


def test_reject_no_explicit_blind_attestation():
    locked, a, b, p = fake_reviews_and_predictions()
    b["reviewer"]["blind_to_system_predictions"] = False
    with pytest.raises(EvidenceGateBlocked, match="blindness attestation"):
        ready_for_scoring(locked, a, b, p)


def test_reject_missing_independent_source_reanalysis():
    locked, a, b, p = fake_reviews_and_predictions()
    a["claims"][4]["independent_reanalysis_reference"] = None
    with pytest.raises(EvidenceGateBlocked, match="missing independent_reanalysis_reference"):
        ready_for_scoring(locked, a, b, p)


def test_reject_mismatched_original_source_hash():
    locked, a, b, p = fake_reviews_and_predictions()
    a["claims"][0]["source_report_sha256"] = "0"*64
    with pytest.raises(EvidenceGateBlocked, match="source hash"):
        ready_for_scoring(locked, a, b, p)


def test_reject_missing_claim_or_extra_claim():
    locked, a, b, p = fake_reviews_and_predictions()
    a["claims"].pop()
    with pytest.raises(EvidenceGateBlocked, match="cover all 24"):
        ready_for_scoring(locked, a, b, p)


def test_reject_disagreement_needing_adjudication():
    locked, a, b, p = fake_reviews_and_predictions()
    b["claims"][0]["gold_label"] = "ERROR_GOLD"
    with pytest.raises(EvidenceGateBlocked, match="adjudication required"):
        ready_for_scoring(locked, a, b, p)


def test_reject_missing_prediction():
    locked, a, b, p = fake_reviews_and_predictions()
    p["naive"].pop()
    with pytest.raises(EvidenceGateBlocked, match="cover all 24"):
        ready_for_scoring(locked, a, b, p)


def test_reject_unknown_predictions():
    locked, a, b, p = fake_reviews_and_predictions()
    p["auditcal"][0]["status"] = "ACCURATE"
    with pytest.raises(EvidenceGateBlocked, match="invalid status"):
        ready_for_scoring(locked, a, b, p)


def test_confusion_metrics_and_abstentions_with_synthetic_cases():
    gold = {
        "A": "ERROR_GOLD", "B": "ERROR_GOLD",
        "C": "SUPPORTED_GOLD", "D": "SUPPORTED_GOLD",
        "E": "INSUFFICIENT_GOLD"
    }
    pred = {
        "A": "FLAGGED_DISCREPANCY", "B": "UNVERIFIABLE",
        "C": "FLAGGED_DISCREPANCY", "D": "SUPPORTED",
        "E": "UNVERIFIABLE"
    }
    z = score(gold, pred)
    assert z["error_recall_abstain_counts_as_miss"]["rate"] == 0.5
    assert z["false_flag_rate_on_supported"]["rate"] == 0.5
    assert z["error_flag_precision_gold_checkable"]["rate"] == 0.5
    assert z["coverage_all"]["rate"] == 0.6
    assert z["unsafe_decisions_on_insufficient"]["numerator"] == 0
    assert z["abstention_rate_on_insufficient"]["rate"] == 1


def test_synthetic_method_difference_reveals_naive_false_flag_mechanism():
    """Known by construction, NOT measured on any new real-world claim."""
    record = {
        "claim_id": "synthetic-only",
        "claim_type": "p_value",
        "reported": 0.01,
        "verified": 0.20,
        "model_id": "method-A",
        "evidence_model_id": "method-B",
        "provenance": {"source": "synthetic smoke-test input"},
        "tolerance": 0.005
    }
    guarded = audit(record).status
    naive = audit({**record, "evidence_model_id": "method-A"}).status
    assert guarded == ABSTAIN
    assert naive == FLAGGED
