"""Regression tests using a VERIFIED fixed snapshot of ONE real AI report.

Not independent evaluation: claim selection and annotation are manual.
"""
import copy
import json
from pathlib import Path

from auditcal import FLAGGED, SUPPORTED
from experiments import audit_authentic_metr_claims as real_audit

RESULT = Path(__file__).resolve().parents[1] / "results/metr_independent_reanalysis_verified.json"

def test_actual_genuine_agent_report_has_eight_supported_mapped_claims():
    source = json.loads(RESULT.read_text(encoding="utf-8"))
    assert source["dataset_sha256_downloaded_bytes"] == "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
    result = real_audit.evaluate_released_report(source)
    assert result["summary"]["total_manually_transcribed_numerical_claims"] == 8
    assert result["summary"]["supported_under_matched_model"] == 8
    assert result["summary"]["flagged_discrepancies"] == 0
    assert all(row["status"] == SUPPORTED for row in result["claims"])

def test_separate_injected_wrong_p_value_is_flagged_not_real_ai_error(monkeypatch):
    source = json.loads(RESULT.read_text(encoding="utf-8"))
    altered = copy.deepcopy(real_audit.REPORTED)
    altered["primary"]["p_value"] = 0.5000
    monkeypatch.setattr(real_audit, "REPORTED", altered)
    result = real_audit.evaluate_released_report(source)
    assert result["summary"]["flagged_discrepancies"] == 1
    assert result["summary"]["supported_under_matched_model"] == 7
    assert next(c for c in result["claims"] if c["claim_id"]=="genuine_agent_primary_p_value")["status"] == FLAGGED
