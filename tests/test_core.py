from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN

BASE = {"claim_id": "T1", "model_id": "ols_a", "evidence_model_id": "ols_a", "provenance": {"source": "human_authored_test_fixture"}}
def check(kind, reported, verified, **extra):
    return audit({**BASE, "claim_type": kind, "reported": reported, "verified": verified, **extra})

def test_matching_coefficient(): assert check("coefficient", 2.0, 2.0).status == SUPPORTED
def test_bad_coefficient(): assert check("coefficient", 2.0, -2.0).status == FLAGGED
def test_near_coefficient(): assert check("coefficient", 2.00001, 2.0).status == SUPPORTED
def test_wrong_sign(): assert check("sign", "positive", -2.0).status == FLAGGED
def test_right_sign(): assert check("sign", "negative", -2.0).status == SUPPORTED
def test_bad_p_value(): assert check("p_value", 0.01, 0.12).status == FLAGGED
def test_missing_p_value(): assert check("p_value", 0.01, None).status == ABSTAIN
def test_pvalue_outside_range(): assert check("p_value", 1.7, 0.2).status == FLAGGED
def test_confidence_interval_match(): assert check("confidence_interval", [-0.2, 0.5], [-0.2, 0.5]).status == SUPPORTED
def test_confidence_interval_disagree(): assert check("confidence_interval", [0.2, 0.5], [-0.2, 0.5]).status == FLAGGED
def test_causal_abstention(): assert check("causal", True, True).status == ABSTAIN
def test_different_models_abstention(): assert check("p_value", 0.01, 0.2, evidence_model_id="ols_b").status == ABSTAIN
def test_provenance_missing(): assert check("p_value", 0.01, 0.01, provenance={}).status == ABSTAIN
def test_sig_correct(): assert check("significant", False, 0.08).status == SUPPORTED
def test_sig_wrong(): assert check("significant", True, 0.08).status == FLAGGED
def test_sig_boundary(): assert check("significant", False, 0.05).status == SUPPORTED
def test_missing_model(): assert check("coefficient", 1, 1, model_id=None).status == ABSTAIN
def test_invalid_tolerance(): assert check("coefficient", 1, 1, tolerance=-1).status == ABSTAIN
def test_non_numeric(): assert check("coefficient", "abc", 3).status == ABSTAIN
def test_int_n(): assert check("sample_size", 42, 42).status == SUPPORTED
def test_invalid_n(): assert check("sample_size", 42.5, 42).status == FLAGGED
def test_unknown_claim(): assert check("fictional", 1, 1).status == ABSTAIN

def test_valid_odds_ratio(): assert check("odds_ratio", 1.246, 1.246213, tolerance=0.0005).status == SUPPORTED
def test_mismatched_odds_ratio(): assert check("odds_ratio", 1.24, 1.50, tolerance=0.001).status == FLAGGED
def test_invalid_reported_odds_ratio(): assert check("odds_ratio", -1, 1.25).status == FLAGGED
def test_invalid_evidence_odds_ratio(): assert check("odds_ratio", 1.25, 0).status == ABSTAIN
