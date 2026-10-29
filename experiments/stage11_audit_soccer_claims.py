"""Run AuditCal on manually mapped, independently calculated real soccer claims.

No released AI code executes, and missing or mismatched estimands abstain.
"""
import json
from pathlib import Path
from auditcal import audit, SUPPORTED, FLAGGED, ABSTAIN
from experiments.stage10_audit_verified_count_claims import evaluate_count_claims

SOURCE=Path("results/stage11_soccer_independent_models.json")
OUT=Path("results/stage11_soccer_auditcal_claims.json")

def one(tag,kind,reported,verified,tolerance=0.0,aligned=True):
    model="soccer:"+tag
    item={"claim_id":tag+":"+kind+":"+str(len(rows)),
          "claim_type":kind, "reported":reported, "verified":verified,
          "model_id":model,"evidence_model_id":model if aligned else model+":UNRESOLVED",
          "tolerance":tolerance,
          "provenance":{"source":"published_hash_verified_claude_soccer_report_pinned_independent_GLM",
                        "dataset_sha256":source["data_copy_sha256"],
                        "report_sha256":source["original_AI_report_sha256"].get(tag.split(":")[0]),
                        "selection_and_method":model}}
    status=audit(item)
    rows.append({**status.to_dict(),"reported":reported,"independent":verified,
                 "tolerance":tolerance})

def source_checks():
    expected={
       "claude_171055":{"n":116160,"light_n":89502,"dark_n":26658,"events":1457,
                        "odds_ratio":1.1574,"odds_ratio_cluster_p":.0570,
                        "odds_ratio_ci":[.9956,1.3454]},
       "claude_173015":{"n":107606,"light_n":90116,"dark_n":17490,
                        "unique_players":1359,"unique_referees":2834,"events":1344,
                        "odds_ratio":1.246,"odds_ratio_cluster_p":.0158,
                        "odds_ratio_ci":[1.042,1.490]}
    }
    for key,claims in expected.items():
        numbers=source["reports"][key]["independent"]
        spec=key+":logistic:by-player-cluster"
        same_sample=numbers["n"]==claims["n"]
        for name,reported in claims.items():
            kind=("confidence_interval" if name=="odds_ratio_ci" else
                  "p_value" if name=="odds_ratio_cluster_p" else
                  "odds_ratio" if name=="odds_ratio" else
                  "distinct_count" if name.startswith("unique_") else "sample_size")
            tol=(.00005 if name in ("odds_ratio_cluster_p",) else
                 .0005 if key=="claude_173015" and name in ("odds_ratio","odds_ratio_ci") else
                 .00005 if name in ("odds_ratio","odds_ratio_ci") else 0)
            one(spec+":"+name,kind,reported,numbers[name],tol,
                aligned=(same_sample or name=="n"))
        if key=="claude_171055":
            one(spec+":bootstrap_p","p_value",.0200,None,aligned=True)
            one(spec+":bootstrap_ci","confidence_interval",[.000269,.003553],None,aligned=True)
        else:
            # Released prose describes discrete exposure contrast, source script
            # calculates derivative AME instead. Do not conflate them.
            one(spec+":RD_description","coefficient",.0027,
                numbers["derivative_risk_difference"],.00005,aligned=False)
            one(spec+":RD_p_description","p_value",.0158,
                numbers["derivative_delta_p"],.00005,aligned=False)

def main():
    global rows,source
    source=json.loads(SOURCE.read_text())
    if source["data_copy_sha256"]!="6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a":
        raise ValueError("Unverified data origin")
    if source["original_AI_code_executed"]: raise ValueError("Original AI code execution prohibited")
    rows=[]
    source_checks()
    first=len(rows)
    qwen=evaluate_count_claims()
    for record in qwen["claims"]:
        rows.append({**record,"from_existing_verified_count_snapshot":True})
    outcome={
        "scope":"three authentic AI-agent Soccer reports, two Claude regression fits and one earlier Qwen count audit",
        "dataset_copy_sha256":source["data_copy_sha256"],
        "original_OSF_bytes_matched":False,
        "source_agent_code_executed":False,
        "claims_manually_mapped":True,
        "claims_from_current_independent_soccer_models":first,
        "claims_from_prior_verified_qwen_count_reanalysis":len(qwen["claims"]),
        "selected_claim_total":len(rows),
        "supported":sum(t["status"]==SUPPORTED for t in rows),
        "flagged":sum(t["status"]==FLAGGED for t in rows),
        "abstained":sum(t["status"]==ABSTAIN for t in rows),
        "scientific_causal_errors_claimed":0,
        "generalization_metrics_justified":False,
        "audits":rows}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(outcome,indent=2)+"\n")
    print("STAGE11_AUDIT_SUMMARY",json.dumps({k:v for k,v in outcome.items() if k!="audits"}),flush=True)
    for result in rows:
        print("STAGE11_CLAIM",json.dumps(result),flush=True)
    if outcome["supported"]!=17 or outcome["flagged"]!=2 or outcome["abstained"]!=4:
        raise RuntimeError("Unexpected claim status distribution: investigate upstream data and source alignment")

if __name__=="__main__": main()
