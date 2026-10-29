"""Only synthetic numeric inputs; no held-out report performance measured."""
from auditcal import audit
from evaluation.naive_values_baseline import compare_values_only

def case(kind, reported, verified, **extras):
    return compare_values_only({"claim_id":"synthetic",
        "claim_type":kind, "reported":reported, "verified":verified,
        "same_units":True, **extras})["status"]

def test_exact_source_count_and_error():
    assert case("distinct_count", 12, 12) == "SUPPORTED"
    assert case("sample_size", 12, 13) == "FLAGGED_DISCREPANCY"

def test_invalid_source_count_requires_abstention():
    assert case("distinct_count", 12, 12.7) == "UNVERIFIABLE"

def test_reported_invalid_count_is_flagged():
    assert case("sample_size", -5, 10) == "FLAGGED_DISCREPANCY"

def test_display_precision_is_fixed_not_tuned_after_outcome():
    assert case("coefficient", 1.133, 1.1334766, display_decimals=3) == "SUPPORTED"
    assert case("coefficient", 1.133, 1.1337000, display_decimals=3) == "FLAGGED_DISCREPANCY"
    assert case("coefficient", 1.133, 1.1334766) == "UNVERIFIABLE"

def test_upper_ci_strict_boundary_in_synthetic_input():
    assert case("confidence_interval", [0.990, 1.351], [0.990497, 1.351514],
        endpoint_decimals=[3,3]) == "FLAGGED_DISCREPANCY"
    assert case("confidence_interval", [0.990, 1.351], [0.990497, 1.351498],
        endpoint_decimals=[3,3]) == "SUPPORTED"

def test_ci_endpoint_precision_must_be_documented():
    assert case("confidence_interval", [0.1,0.2], [0.1,0.2]) == "UNVERIFIABLE"

def test_equal_units_are_required():
    assert compare_values_only({"claim_type":"coefficient","claim_id":"synthetic",
        "reported":0.1,"verified":0.2,"display_decimals":2})["status"] == "UNVERIFIABLE"

def test_invalid_p_evidence_abstains():
    assert case("p_value", 0.12, 1.4, display_decimals=2) == "UNVERIFIABLE"

def test_valid_p_value_rounding():
    assert case("p_value", 0.066, 0.065837, display_decimals=3) == "SUPPORTED"

def test_model_mismatch_baseline_limitation_by_construction():
    """This demonstrates code semantics only, not real-world false alarms."""
    record={"claim_id":"synthetic","claim_type":"coefficient",
            "reported":1.1,"verified":1.6, "same_units":True, "display_decimals":1,
            "model_id":"A","evidence_model_id":"B",
            "provenance":{"source":"artificial fixture"}}
    assert compare_values_only(record)["status"] == "FLAGGED_DISCREPANCY"
    assert audit(record).status == "UNVERIFIABLE"
