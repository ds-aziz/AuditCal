"""Predeclared simple values-only comparator for source-evidence numeric claims.

This baseline deliberately DOES NOT check statistical model/sample/estimand
identity. It *does* require units to be normalized and the same independently
computed evidence to be provided as for AuditCal. Missing evidence -> abstain.

WARNING: this is NOT a research run or measured reliability score. The script
is implemented after the 24 reports' preliminary outcomes were investigated.
Any application to that same pilot must be labelled retrospective/exploratory.
An unbiased evaluation of newly developed code needs fresh untouched reports.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

SUPPORTED = "SUPPORTED"
FLAGGED = "FLAGGED_DISCREPANCY"
ABSTAIN = "UNVERIFIABLE"

NUMERIC_KINDS = {"coefficient", "odds_ratio", "p_value", "sample_size", "distinct_count"}
COUNT_KINDS = {"sample_size", "distinct_count"}


def _dec(x: Any) -> Decimal | None:
    if isinstance(x, bool) or x is None:
        return None
    try:
        v = Decimal(str(x))
        return v if v.is_finite() else None
    except (TypeError, InvalidOperation, ValueError):
        return None


def _valid_precision(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= 12


def _within_display_rounding(a: Decimal, b: Decimal, decimals: int) -> bool:
    """Frozen interval: half a display unit, with <= 1e-8 absolute boundary pad."""
    half = Decimal("0.5") * (Decimal(10) ** -decimals)
    return abs(a - b) <= half + Decimal("0.00000001")


def compare_values_only(record: dict) -> dict[str, str]:
    """Return a typed decision without inspecting model_id/evidence_model_id.

    Input is source-matched evidence with units already normalized by a human.
    This intentionally does NOT verify whether source *method* was the same.
    """
    cid = str(record.get("claim_id", "unknown"))
    kind = record.get("claim_type")
    def result(status: str, reason: str) -> dict[str, str]:
        return {"claim_id": cid, "status": status, "reason": reason}
    if kind not in NUMERIC_KINDS | {"confidence_interval"}:
        return result(ABSTAIN, "Outside predeclared values-only numeric baseline scope")
    if record.get("same_units") is not True:
        return result(ABSTAIN, "Source and claim units not documented as identical")
    reported, verified = record.get("reported"), record.get("verified")
    if kind == "confidence_interval":
        if (not isinstance(reported, (list, tuple)) or not isinstance(verified, (list, tuple))
            or len(reported) != 2 or len(verified) != 2):
            return result(ABSTAIN, "Interval or numeric source evidence is missing")
        x = [_dec(v) for v in [*reported, *verified]]
        prec = record.get("endpoint_decimals")
        if (any(z is None for z in x) or not isinstance(prec, list)
            or len(prec) != 2 or not all(_valid_precision(v) for v in prec)):
            return result(ABSTAIN, "Interval or source-quoted endpoint precision missing")
        rlo, rhi, vlo, vhi = x
        if rlo > rhi or vlo > vhi:
            return result(ABSTAIN, "Malformed confidence interval ordering")
        ok = (_within_display_rounding(rlo, vlo, prec[0]) and
              _within_display_rounding(rhi, vhi, prec[1]))
        return result(SUPPORTED if ok else FLAGGED,
                      "Interval numerically agrees to frozen display precision" if ok
                      else "Different interval values; model equivalence NOT checked")
    r, v = _dec(reported), _dec(verified)
    if r is None or v is None:
        return result(ABSTAIN, "Reported value or computed source evidence missing")
    if kind in COUNT_KINDS:
        if v < 0 or v != v.to_integral_value():
            return result(ABSTAIN, "Source count invalid")
        if r < 0 or r != r.to_integral_value():
            return result(FLAGGED, "Reported count is not a valid nonnegative whole number")
        ok = r == v
    else:
        if kind == "odds_ratio":
            if v <= 0:
                return result(ABSTAIN, "Invalid computed odds ratio")
            if r <= 0:
                return result(FLAGGED, "Reported odds ratio must be positive")
        if kind == "p_value":
            if not Decimal(0) <= v <= Decimal(1):
                return result(ABSTAIN, "Invalid computed p-value")
            if not Decimal(0) <= r <= Decimal(1):
                return result(FLAGGED, "Reported p-value outside zero-one range")
        precision = record.get("display_decimals")
        if not _valid_precision(precision):
            return result(ABSTAIN, "Frozen source-quoted display precision missing")
        ok = _within_display_rounding(r, v, precision)
    return result(SUPPORTED if ok else FLAGGED,
                  "Number agrees to frozen displayed precision" if ok
                  else "Values differ numerically; different valid method is NOT checked")
