"""Guarded evaluation scorer for the FROZEN 24-claim AuditCal pilot.

This code does NOT obtain independent human labels, assign them, re-run any
source analysis, or infer model equivalence. It *refuses* to score unless two
distinct, attested human reviewers supply complete blind labels for the
same 24 frozen source claims AND reproducible predictions are provided.

Reviewer attestations here are machine-readable declarations; they cannot
cryptographically prove that an independent human actually reviewed a claim.
Check that evidence outside this program before scholarly reporting.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "evaluation" / "heldout_v01_selected_claims.json"
GOLD = ("SUPPORTED_GOLD", "ERROR_GOLD", "INSUFFICIENT_GOLD")
PRED = ("SUPPORTED", "FLAGGED_DISCREPANCY", "UNVERIFIABLE")


class EvidenceGateBlocked(ValueError):
    """Scoring cannot begin without locked, independent admissible evidence."""


def frozen_claims(path: Path = FROZEN) -> dict[str, dict]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("version") != "heldout_v01_first3_claims":
        raise EvidenceGateBlocked("Wrong frozen pilot manifest version")
    claims = obj.get("claims")
    if not isinstance(claims, list) or len(claims) != 24:
        raise EvidenceGateBlocked("Frozen pilot must contain exactly 24 claims")
    ids = [v.get("claim_id") for v in claims if isinstance(v, dict)]
    if len(ids) != 24 or len(set(ids)) != 24:
        raise EvidenceGateBlocked("Frozen pilot contains duplicate or invalid IDs")
    return {v["claim_id"]: v for v in claims}


def _exact_rows(rows: Any, field: str, frozen: dict[str, dict]) -> dict[str, dict]:
    if not isinstance(rows, list) or len(rows) != len(frozen):
        raise EvidenceGateBlocked(f"{field} must cover all {len(frozen)} frozen claims")
    result: dict[str, dict] = {}
    for r in rows:
        if not isinstance(r, dict) or not isinstance(r.get("claim_id"), str):
            raise EvidenceGateBlocked(f"{field}: invalid claim row")
        cid = r["claim_id"]
        if cid in result:
            raise EvidenceGateBlocked(f"{field}: duplicate claim {cid}")
        result[cid] = r
    if result.keys() != frozen.keys():
        raise EvidenceGateBlocked(f"{field}: missing or unexpected claim IDs")
    return result


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and len(value.strip()) >= 3


def _check_review(obj: dict, frozen: dict[str, dict], tag: str) -> tuple[str, dict[str, str]]:
    reviewer = obj.get("reviewer")
    if not isinstance(reviewer, dict):
        raise EvidenceGateBlocked(f"{tag}: signed reviewer metadata missing")
    for key in ("reviewer_id", "name", "signed_date", "signed_attestation"):
        if not _nonempty(reviewer.get(key)):
            raise EvidenceGateBlocked(f"{tag}: missing {key}")
    for key in ("independent_human", "blind_to_system_predictions",
                "no_involvement_in_auditcal_development"):
        if reviewer.get(key) is not True:
            raise EvidenceGateBlocked(f"{tag}: explicit human/blindness attestation {key} missing")
    rows = _exact_rows(obj.get("claims"), tag, frozen)
    labels = {}
    for cid, row in rows.items():
        if row.get("source_report_sha256") != frozen[cid]["source_report_sha256"]:
            raise EvidenceGateBlocked(f"{tag}/{cid}: source hash not frozen hash")
        if row.get("gold_label") not in GOLD:
            raise EvidenceGateBlocked(f"{tag}/{cid}: invalid or missing gold label")
        for key in ("independent_reanalysis_reference", "source_method_reference", "rationale"):
            if not _nonempty(row.get(key)):
                raise EvidenceGateBlocked(f"{tag}/{cid}: missing {key}")
        labels[cid] = row["gold_label"]
    return reviewer["reviewer_id"], labels


def double_reviewed_labels(
    frozen: dict[str, dict], first: dict, second: dict
) -> dict[str, str]:
    id1, labels1 = _check_review(first, frozen, "review_1")
    id2, labels2 = _check_review(second, frozen, "review_2")
    if id1 == id2:
        raise EvidenceGateBlocked("Reviewers must have distinct identities")
    conflicts = [cid for cid in frozen if labels1[cid] != labels2[cid]]
    if conflicts:
        raise EvidenceGateBlocked(
            "Human review disagreement remains; independent adjudication required "
            "before scoring: " + ", ".join(conflicts)
        )
    return labels1


def _predictions(obj: dict, frozen: dict[str, dict]) -> dict[str, dict[str, str]]:
    m = obj.get("run_metadata")
    if not isinstance(m, dict):
        raise EvidenceGateBlocked("Missing paired prediction reproducibility metadata")
    for key in ("auditcal_code_commit", "baseline_code_commit",
                "source_evidence_manifest", "run_log_url"):
        if not _nonempty(m.get(key)):
            raise EvidenceGateBlocked("Missing prediction provenance: " + key)
    outputs = {}
    for which in ("auditcal", "naive"):
        values = _exact_rows(obj.get(which), which, frozen)
        statuses = {}
        for cid, v in values.items():
            if v.get("status") not in PRED:
                raise EvidenceGateBlocked(f"{which}/{cid}: invalid status")
            if not _nonempty(v.get("reason")):
                raise EvidenceGateBlocked(f"{which}/{cid}: decision reason missing")
            statuses[cid] = v["status"]
        outputs[which] = statuses
    return outputs


def _rate(numerator: int, denominator: int) -> dict:
    """Wilson 95% interval; None if denominator zero."""
    if not denominator:
        return {"numerator": numerator, "denominator": denominator,
                "rate": None, "wilson_95": None}
    p = numerator / denominator
    z = 1.959963984540054
    d = 1 + z*z/denominator
    center = (p + z*z/(2*denominator)) / d
    spread = z * math.sqrt(p*(1-p)/denominator + z*z/(4*denominator*denominator)) / d
    return {"numerator": numerator, "denominator": denominator, "rate": p,
            "wilson_95": [max(0, center-spread), min(1, center+spread)]}


def score(labels: dict[str, str], predictions: dict[str, str]) -> dict:
    if labels.keys() != predictions.keys():
        raise EvidenceGateBlocked("gold and prediction claim sets differ")
    matrix = {gold: {status: 0 for status in PRED} for gold in GOLD}
    for cid in labels:
        matrix[labels[cid]][predictions[cid]] += 1
    cases = list(labels)
    no_insuff = [cid for cid in cases if labels[cid] != "INSUFFICIENT_GOLD"]
    actual_errors = [cid for cid in cases if labels[cid] == "ERROR_GOLD"]
    actual_supported = [cid for cid in cases if labels[cid] == "SUPPORTED_GOLD"]
    actual_unknown = [cid for cid in cases if labels[cid] == "INSUFFICIENT_GOLD"]
    decisive = [cid for cid in cases if predictions[cid] != "UNVERIFIABLE"]
    decisive_checkable = [cid for cid in no_insuff if predictions[cid] != "UNVERIFIABLE"]
    flags_checkable = [cid for cid in no_insuff if predictions[cid] == "FLAGGED_DISCREPANCY"]
    return {
        "confusion_3x3": matrix,
        "all_selected_claims": len(cases),
        "gold_class_counts": dict(Counter(labels.values())),
        "coverage_all": _rate(len(decisive), len(cases)),
        "coverage_gold_checkable": _rate(len(decisive_checkable), len(no_insuff)),
        "error_flag_precision_gold_checkable": _rate(
            sum(labels[cid] == "ERROR_GOLD" for cid in flags_checkable),
            len(flags_checkable)),
        "error_recall_abstain_counts_as_miss": _rate(
            sum(predictions[cid] == "FLAGGED_DISCREPANCY" for cid in actual_errors),
            len(actual_errors)),
        "false_flag_rate_on_supported": _rate(
            sum(predictions[cid] == "FLAGGED_DISCREPANCY" for cid in actual_supported),
            len(actual_supported)),
        "unsafe_decisions_on_insufficient": _rate(
            sum(predictions[cid] != "UNVERIFIABLE" for cid in actual_unknown),
            len(actual_unknown)),
        "abstention_rate_on_insufficient": _rate(
            sum(predictions[cid] == "UNVERIFIABLE" for cid in actual_unknown),
            len(actual_unknown))
    }


def ready_for_scoring(
    frozen: dict[str, dict], review1: dict, review2: dict, prediction_file: dict
) -> dict:
    labels = double_reviewed_labels(frozen, review1, review2)
    both = _predictions(prediction_file, frozen)
    return {
        "status": "GATED_HUMAN_ATTESTED_DESCRIPTIVE_PILOT",
        "evidence_warning": (
            "Reviewer identity, expertise, signatures and genuinely blind independent "
            "human analysis MUST also be verified outside software; this module "
            "checks declarations, not the truth of identities. This is a small "
            "report-held-out pilot on familiar datasets, not general accuracy."
        ),
        "reports_selected": 8,
        "claims_selected": len(frozen),
        "auditcal": score(labels, both["auditcal"]),
        "naive": score(labels, both["naive"]),
        "paired_cases": [
            {"claim_id": cid, "report_id": frozen[cid]["report_id"],
             "gold_label": labels[cid], "auditcal": both["auditcal"][cid],
             "naive": both["naive"][cid]}
            for cid in frozen
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--review-one", type=Path)
    p.add_argument("--review-two", type=Path)
    p.add_argument("--predictions", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    frozen = frozen_claims()
    files = (args.review_one, args.review_two, args.predictions)
    if not all(files):
        print(json.dumps({
            "status": "BLOCKED_PENDING_INDEPENDENT_GOLD_AND_PAIRED_PREDICTIONS",
            "frozen_claims": len(frozen),
            "no_accuracy_calculated": True,
            "missing": [
                "two fully independent human reviewer sheets for ALL 24 claims",
                "reconciled disagreements / valid signed adjudication",
                "source-logged paired AuditCal and naive comparator predictions"
            ],
        }, indent=2))
        return
    try:
        review1, review2, preds = [
            json.loads(path.read_text(encoding="utf-8")) for path in files
        ]
        result = ready_for_scoring(frozen, review1, review2, preds)
    except (EvidenceGateBlocked, FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit("EVALUATION BLOCKED: " + str(exc)) from exc
    serialized = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
