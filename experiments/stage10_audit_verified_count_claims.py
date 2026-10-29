"""Audit three source-matched counts quoted in one real Qwen3 soccer report.

Claims were manually extracted from the source report and original sample
construction independently reproduced using a pinned published CSV copy.
No published model code is executed. This is a data-count check only.
"""
import json
from pathlib import Path
from auditcal import audit, SUPPORTED, FLAGGED

SOURCE = Path(__file__).resolve().parents[1] / "results/stage10_source_count_verified.json"

def evaluate_count_claims():
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    if data["independent_calc_conclusion"] != "success":
        raise ValueError("Cannot use a failed source-reconstruction run")
    filtered=data["independent_reimplementation_of_reported_selection"]
    expected_model={
        "players":"soccer:Qwen3:mean-skin-extremes:complete-case:unique-playerShort",
        "referees":"soccer:Qwen3:mean-skin-extremes:complete-case:unique-refNum",
        "dyads":"soccer:Qwen3:mean-skin-extremes:complete-case:row-count",
    }
    checks=[
        ("unique_players", 9959, filtered["retained_unique_players"], "players", "distinct_count"),
        ("unique_referees", 2103, filtered["retained_unique_referees"], "referees", "distinct_count"),
        ("dyad_count", data["reported_final_dyads"], filtered["retained_dyads"], "dyads", "sample_size")
    ]
    rows=[]
    for label,reported,verified,model_key,kind in checks:
        model=expected_model[model_key]
        record={
            "claim_id":f"genuine_qwen_soccer_{label}",
            "claim_type":kind,"reported":reported,"verified":verified,
            "model_id":model,"evidence_model_id":model,
            "provenance":{
                "source":"verified_public_Qwen3_agent_report_and_pinned_soccer_dataset_copy",
                "report_sha256":data["source_report_sha256"],
                "dataset_copy_sha256":data["source_data_sha256"],
                "sample_filter":"both raters present, <=.25 or >=.75, complete model rows",
                "source_calculation_run":data["independent_calc_workflow"]
            },
        }
        result=audit(record)
        rows.append({**result.to_dict(),"reported":reported,"source_derived":verified,
                     "note":"Manual claim extraction; exact model selection and evidence provenance supplied"})
    return {
        "source":"one independently hash-verified published agent report, Qwen3 235B, sample_soccer",
        "genuine_report_claims_checked":len(rows),
        "flagged_data_count_mismatches":sum(x["status"] == FLAGGED for x in rows),
        "supported_reported_sample_counts":sum(x["status"] == SUPPORTED for x in rows),
        "confirmed_statistical_model_errors":0,
        "independently_blind_annotated":False,
        "original_OSF_bytes_not_checked":True,
        "agent_code_never_executed":True,
        "report_location":data["report_statement_location"],
        "claims":rows
    }

def main():
    output=evaluate_count_claims()
    target=Path("results/stage10_genuine_agent_distinct_count_claims.json")
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print("REAL_REPORT_COUNT_CLAIMS",json.dumps(output,ensure_ascii=False),flush=True)
    if (output["flagged_data_count_mismatches"] != 2
        or output["supported_reported_sample_counts"] != 1):
        raise SystemExit("Original real report count checks do not match independently calculated data")

if __name__=="__main__":
    main()
