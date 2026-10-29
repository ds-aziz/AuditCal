"""Conservative evidence-based checks for structured statistical claims.

No free-text extraction, code execution, or scientific validity certification.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import isfinite
from typing import Any

ALLOWED_KINDS = {"coefficient", "odds_ratio", "p_value", "sample_size", "distinct_count", "sign", "significant", "confidence_interval", "causal"}
SUPPORTED = "SUPPORTED"
FLAGGED = "FLAGGED_DISCREPANCY"
ABSTAIN = "UNVERIFIABLE"

@dataclass(frozen=True)
class AuditResult:
    claim_id: str
    status: str
    reason: str
    claim_type: str
    model_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        result = float(value)
        return result if isfinite(result) else None
    except (TypeError, ValueError, OverflowError):
        return None

def audit(record: dict[str, Any]) -> AuditResult:
    """Compare reported value with externally supplied model-matched evidence.

    'verified' is supplied by the caller; this module does not independently
    derive it from any dataset.
    """
    claim_id = str(record.get("claim_id", "unknown"))
    kind = str(record.get("claim_type", "unknown"))
    model_id = record.get("model_id")
    def result(status: str, reason: str) -> AuditResult:
        return AuditResult(claim_id, status, reason, kind, str(model_id) if model_id is not None else None)

    if kind not in ALLOWED_KINDS:
        return result(ABSTAIN, "Unknown claim type; no defensible automated check")
    if kind == "causal":
        return result(ABSTAIN, "A numerical match cannot establish causal identification")
    if not isinstance(record.get("provenance"), dict) or not record["provenance"].get("source"):
        return result(ABSTAIN, "Missing provenance for evidence")
    if not model_id or not record.get("evidence_model_id"):
        return result(ABSTAIN, "Model identity missing; cannot align estimands")
    if str(model_id) != str(record.get("evidence_model_id")):
        return result(ABSTAIN, "Different model specifications; valid alternative analysis is possible")
    reported, verified = record.get("reported"), record.get("verified")
    if kind == "confidence_interval":
        if not (isinstance(reported, list) and isinstance(verified, list) and len(reported) == len(verified) == 2):
            return result(ABSTAIN, "Malformed or missing confidence interval")
        vals = [_number(x) for x in (reported + verified)]
        if any(x is None for x in vals):
            return result(ABSTAIN, "Missing/non-numeric confidence interval")
        rlo, rhi, vlo, vhi = vals
        if rlo > rhi or vlo > vhi:
            return result(ABSTAIN, "Invalid confidence interval order")
        tol = _number(record.get("tolerance", 1e-4))
        if tol is None or tol < 0:
            return result(ABSTAIN, "Invalid tolerance")
        ok = abs(rlo-vlo) <= tol and abs(rhi-vhi) <= tol
        return result(SUPPORTED if ok else FLAGGED, "Reported interval matches model-aligned evidence" if ok else "Interval differs from model-aligned evidence")
    if kind in {"coefficient", "odds_ratio", "p_value", "sample_size", "distinct_count", "significant", "sign"}:
        evidence = _number(verified)
        if evidence is None:
            return result(ABSTAIN, "Verified numerical evidence missing or invalid")
        if kind in {"sample_size", "distinct_count"} and (evidence < 0 or not evidence.is_integer()):
            return result(ABSTAIN, "Evidence count is not a nonnegative integer")
        if kind == "odds_ratio" and evidence <= 0:
            return result(ABSTAIN, "Evidence odds ratio must be strictly positive")
        if kind == "p_value" and not (0 <= evidence <= 1):
            return result(ABSTAIN, "Evidence p-value outside [0, 1]")
        if kind == "significant":
            if not isinstance(reported, bool):
                return result(ABSTAIN, "Significance claim must be true or false")
            alpha = _number(record.get("alpha", 0.05))
            if alpha is None or not (0 < alpha < 1) or not (0 <= evidence <= 1):
                return result(ABSTAIN, "Missing/invalid alpha or p-value")
            ok = reported == (evidence < alpha)
        elif kind == "sign":
            if reported not in {"negative", "positive", "zero"}:
                return result(ABSTAIN, "Reported sign must be negative/positive/zero")
            observed = "negative" if evidence < 0 else ("positive" if evidence > 0 else "zero")
            ok = reported == observed
        else:
            claim_value = _number(reported)
            if claim_value is None:
                return result(ABSTAIN, "Reported number missing or invalid")
            if kind == "odds_ratio" and claim_value <= 0:
                return result(FLAGGED, "Reported odds ratio must be strictly positive")
            if kind == "p_value" and not (0 <= claim_value <= 1):
                return result(FLAGGED, "Reported p-value outside [0, 1]")
            if kind in {"sample_size", "distinct_count"} and (claim_value < 0 or not claim_value.is_integer()):
                return result(FLAGGED, "Count must be a nonnegative integer")
            tol = 0.0 if kind in {"sample_size", "distinct_count"} else _number(record.get("tolerance", 1e-4))
            if tol is None or tol < 0:
                return result(ABSTAIN, "Invalid tolerance")
            ok = abs(claim_value-evidence) <= tol
        return result(SUPPORTED if ok else FLAGGED, "Reported claim matches model-aligned evidence" if ok else "Claim differs from model-aligned evidence")
    return result(ABSTAIN, "No check implemented")
