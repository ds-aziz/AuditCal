"""Independently recompute selected numbers in SIX released reports from 3 AI models.

Original agent scripts are never imported or executed. Claims and model
specifications are researcher-transcribed from verified public sources, not
blindly annotated benchmarks.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA_HASH = "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
DATA_URL = ("https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/"
            "blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv")
REPORTED = [
    ("Claude Haiku 4.5", "2025-11-14T14-53-43+0000", 1.1570, 0.0658, "standard"),
    ("Claude Haiku 4.5", "2025-11-14T15-33-39+0000", 1.1570, 0.0670, "standard"),
    ("Qwen3 235B", "2025-12-11T22-20-15+0000", 1.1570, 0.0660, "standard"),
    ("Qwen3 235B", "2025-12-11T22-22-18+0000", 1.1570, 0.0660, "standard"),
    ("Qwen3 Coder 480B", "2025-12-11T22-15-03+0000", 1.1570, 0.0658, "standard"),
    ("Qwen3 Coder 480B", "2025-12-11T22-17-28+0000", 1.1392, 0.1158, "coder_variant"),
]
P_ABS_TOL = 0.003
GMR_ABS_TOL = 0.003

def summarize(fit, frame, formula, transformation):
    b=float(fit.params["ai_treatment"])
    se=float(fit.bse["ai_treatment"])
    return {
        "formula":formula, "outcome_transformation":transformation,
        "n":len(frame),"developers":int(frame["dev_id"].nunique()),
        "beta":b,"gmr_from_transformed_outcome":float(np.exp(b)),
        "p_value":float(fit.pvalues["ai_treatment"]),"se":se,
        "reml":True,"converged":bool(fit.converged),
    }

def independently_check(path:Path):
    content=path.read_bytes()
    checksum=hashlib.sha256(content).hexdigest()
    if checksum!=DATA_HASH:
        raise ValueError("Official METR source data hash mismatch")
    d=pd.read_csv(path)
    assert len(d)==246 and d["dev_id"].nunique()==16
    assert (d["initial_implementation_time"]>0).all()
    assert (d["predicted_time_no_ai"]>0).all()
    assert d["predicted_time_ai_allowed"].notna().all()
    d["log_initial"]=np.log(d["initial_implementation_time"])
    d["log_pred_without_ai"]=np.log(d["predicted_time_no_ai"])
    d["log_initial_plus1"]=np.log1p(d["initial_implementation_time"])
    d["average_predicted_time"]=(d["predicted_time_no_ai"]+
                                  d["predicted_time_ai_allowed"])/2

    canonical_formula="log_initial ~ ai_treatment + log_pred_without_ai"
    canonical=smf.mixedlm(canonical_formula,d,groups=d["dev_id"]).fit(reml=True)
    variant_formula="log_initial_plus1 ~ ai_treatment + average_predicted_time"
    variant=smf.mixedlm(variant_formula,d,groups=d["dev_id"]).fit(reml=True)
    models={
       "standard":summarize(canonical,d,canonical_formula,"natural log of initial minutes"),
       "coder_variant":summarize(variant,d,variant_formula,"natural log of (initial minutes + 1)")
    }
    checks=[]
    for model_name,timestamp,reported_gmr,reported_p,method_key in REPORTED:
        output=models[method_key]
        delta_gmr=output["gmr_from_transformed_outcome"]-reported_gmr
        delta_p=output["p_value"]-reported_p
        within=bool(output["converged"] and
                    abs(delta_gmr)<=GMR_ABS_TOL and abs(delta_p)<=P_ABS_TOL)
        checks.append({
           "ai_model":model_name,"run_id":timestamp,
           "original_report_gmr":reported_gmr,
           "original_report_p_value":reported_p,
           "method_identity_researcher_mapped":method_key,
           "independently_recomputed":output,
           "difference_gmr":delta_gmr,"difference_p":delta_p,
           "numeric_status":("AGREES_WITH_REPORTED_MODEL" if within else
                             "REQUIRES_SOURCE_AND_METHOD_REVIEW"),
           "manual_transcription_not_blind":True
        })
    study={
      "source_dataset":DATA_URL,
      "dataset_sha256":checksum,
      "source_agent_reports":"amazon-science/agentic-forking-path",
      "original_agent_scripts_executed":False,
      "researcher_selected_model_specifications":True,
      "same_model_across_every_comparison":False,
      "report_count":len(checks),
      "distinct_models_tested":3,
      "tolerance_gmr":GMR_ABS_TOL,
      "tolerance_p":P_ABS_TOL,
      "models":models,"checks":checks,
      "methodological_note":(
        "The Qwen3 Coder variant uses log(initial_minutes+1), not "
        "log(initial_minutes). Exponentiating its coefficient estimates "
        "a geometric ratio of (minutes+1), not literally the unshifted "
        "time's geometric mean ratio. Its task-size predictor also differs."
      ),
      "narrative_review_candidate":(
        "A Haiku report says the primary hypothesis is SUPPORTED although its "
        "own reported primary p value is 0.067 (>0.05). Investigate reported "
        "decision rule before labeling the narrative scientifically wrong."
      ),
      "independently_adjudicated_narrative_errors":0,
      "independent_holdout_size":0,
      "status":"EXPLORATORY_NUMERIC_REPLICATION_NOT_BENCHMARK"
    }
    return study

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("csv",type=Path)
    p.add_argument("--output",type=Path,
                   default=Path("results/stage9_three_other_models_reanalysis.json"))
    a=p.parse_args()
    result=independently_check(a.csv)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    for c in result["checks"]:
        print(json.dumps({k:c[k] for k in (
            "ai_model","run_id","original_report_p_value","difference_p","numeric_status")}))
    print("STAGE9_RESULT_JSON",json.dumps(result,separators=(",",":")))
    print("STAGE9_NUMERIC_SUMMARY",
        json.dumps({"n":len(result["checks"]),
             "matching":sum(c["numeric_status"]=="AGREES_WITH_REPORTED_MODEL"
                            for c in result["checks"])}))
    if any(c["numeric_status"]!="AGREES_WITH_REPORTED_MODEL" for c in result["checks"]):
        raise SystemExit("Not every model matches; investigate before asserting success")

if __name__=="__main__":
    main()
