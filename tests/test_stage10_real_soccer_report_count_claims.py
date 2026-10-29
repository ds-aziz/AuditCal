"""Fixed-snapshot tests of a source-verifiable REAL agent reporting inconsistency."""
import json
from pathlib import Path
from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN
from experiments.stage10_audit_verified_count_claims import evaluate_count_claims, SOURCE

def test_two_real_report_count_discrepancies_and_correct_dyad_count():
    result=evaluate_count_claims()
    assert result["genuine_report_claims_checked"]==3
    assert result["flagged_data_count_mismatches"]==2
    assert result["supported_reported_sample_counts"]==1
    rows={x["claim_id"]:x for x in result["claims"]}
    assert rows["genuine_qwen_soccer_unique_players"]["reported"]==9959
    assert rows["genuine_qwen_soccer_unique_players"]["source_derived"]==1214
    assert rows["genuine_qwen_soccer_unique_players"]["status"]==FLAGGED
    assert rows["genuine_qwen_soccer_unique_referees"]["reported"]==2103
    assert rows["genuine_qwen_soccer_unique_referees"]["source_derived"]==2758
    assert rows["genuine_qwen_soccer_unique_referees"]["status"]==FLAGGED
    assert rows["genuine_qwen_soccer_dyad_count"]["reported"]==99535
    assert rows["genuine_qwen_soccer_dyad_count"]["source_derived"]==99535
    assert rows["genuine_qwen_soccer_dyad_count"]["status"]==SUPPORTED

def test_full_data_contains_fewer_players_than_report_claim():
    data=json.loads(SOURCE.read_text())
    assert data["all_source_unique_player_ids"]==2053
    assert data["reported_unique_players"] > data["all_source_unique_player_ids"]
    assert data["all_source_rows"]==146028
    assert data["source_data_sha256"]=="6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"

def test_different_filter_definition_must_abstain():
    r=audit({"claim_id":"mismatch","claim_type":"distinct_count",
        "reported":9959,"verified":1214,
        "model_id":"filter_1","evidence_model_id":"filter_2",
        "provenance":{"source":"pinned public study dataset"}})
    assert r.status==ABSTAIN

def test_bogus_count_evidence_abstains_and_noninteger_report_flags():
    base={"claim_id":"bad_count","claim_type":"distinct_count",
        "model_id":"m1","evidence_model_id":"m1",
        "provenance":{"source":"official dataset"}}
    assert audit({**base,"reported":12,"verified":12.5}).status==ABSTAIN
    assert audit({**base,"reported":12.5,"verified":12}).status==FLAGGED
    assert audit({**base,"reported":12,"verified":12}).status==SUPPORTED
    assert audit({**base,"reported":12,"verified":13}).status==FLAGGED

def test_one_real_report_is_not_full_performance_benchmark():
    result=evaluate_count_claims()
    assert not result["independently_blind_annotated"]
    assert result["confirmed_statistical_model_errors"]==0
    assert result["original_OSF_bytes_not_checked"]
    assert result["agent_code_never_executed"]
