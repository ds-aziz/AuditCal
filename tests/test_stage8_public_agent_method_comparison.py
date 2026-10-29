"""Conservative tests for exploratory genuine-agent numerical reproduction.

These tests use an archived, externally executed independent-method snapshot.
They do not establish that the analysis choices themselves are valid.
"""
import json
from pathlib import Path

from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN

PATH=Path(__file__).resolve().parents[1] / "results/stage8_independent_method_variants_verified.json"

def snapshot():
    x=json.loads(PATH.read_text())
    assert x["dataset_sha256"]=="1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
    assert x["provenance"]["workflow_result"]=="success"
    assert not x["provenance"]["agent_code_executed"]
    return x["methods"]

def claim(reported, verified, model, evidence_model=None, tolerance=0.001):
    return audit({"claim_id":"public_agent_p","claim_type":"p_value",
                  "model_id":model,"evidence_model_id":evidence_model or model,
                  "provenance":{"source":"official_Metr_RCT_public_release"},
                  "reported":reported,"verified":verified,"tolerance":tolerance})

def test_five_reported_primary_p_values_reproduce_when_methods_match():
    m=snapshot()
    examples=[
        (0.0658,m["original_standard_mixed"]["p_value"],"mixed_REML_noAI_pred"),
        (0.4446,m["negative_two_stage_as_reported"]["p_value"],"two_stage_min_norm_all16"),
        (0.245,m["positive_claimed_FE_no_intercept"]["p_value"],"FE_15dummy_no_intercept"),
        (0.022,m["confirmation_ML_other_covariate"]["p_using_task_level_t"],"mixed_ML_ai_pred_t"),
        (0.0210,m["strong_confirmation_nearest_matching"]["p_value"],"nearest_match_15_devs"),
    ]
    assert all(claim(r,v,key).status==SUPPORTED for r,v,key in examples)

def test_legitimate_model_difference_must_not_be_declared_a_numeric_error():
    m=snapshot()
    r=claim(0.022,m["original_standard_mixed"]["p_value"],
            "mixed_ML_ai_pred_t","mixed_REML_noAI_pred")
    assert r.status==ABSTAIN
    assert "Different model specifications" in r.reason

def test_same_method_injected_wrong_number_is_detected_not_an_ai_mistake():
    m=snapshot()
    assert claim(0.7,m["original_standard_mixed"]["p_value"],
                 "mixed_REML_noAI_pred").status==FLAGGED

def test_small_group_regression_is_highly_sensitive_to_exclusion():
    m=snapshot()
    all_=m["negative_two_stage_as_reported"]
    reduced=m["negative_two_stage_excluding_low_information"]
    assert all_["developers_with_effect"]==16
    assert reduced["developers_with_effect"]==15
    assert abs(all_["p_value"]-reduced["p_value"])>0.2

def test_missing_reference_intercept_changes_fixed_effects_specification():
    m=snapshot()
    old=m["positive_claimed_FE_no_intercept"]
    canonical=m["proper_developer_FE_with_intercept"]
    assert canonical["num_parameters"]==old["num_parameters"]+1
    assert abs(canonical["p_value"]-old["p_value"])>0.001
