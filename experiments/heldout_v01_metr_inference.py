"""Independent reanalysis of eight frozen METR statistical claims.

Original AI scripts are never executed. S5's ambiguous formula is treated as
unresolved until independent methodological review.
"""
from __future__ import annotations
import argparse, hashlib, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf

ROOT=Path(__file__).resolve().parents[1]
SHA="1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"

def summarize(fit, label):
    beta=float(fit.params["ai_treatment"])
    ci=np.asarray(fit.conf_int().loc["ai_treatment"])
    gmr=float(np.exp(beta))
    return {"label":label,"beta":beta,"gmr":gmr,
            "percent_change":100*(gmr-1),
            "ci_gmr":[float(np.exp(z)) for z in ci],
            "p":float(fit.pvalues["ai_treatment"]),
            "se":float(fit.bse["ai_treatment"]),
            "converged":bool(getattr(fit,"converged",True))}

def run(path):
    with path.open("rb") as h: digest=hashlib.file_digest(h,"sha256").hexdigest()
    if digest!=SHA:raise ValueError("Official METR SHA256 mismatch")
    d=pd.read_csv(path)
    if len(d)!=246 or d.dev_id.nunique()!=16:raise ValueError("Unrecognized METR data")
    d["log_y"]=np.log(d.initial_implementation_time)
    d["log_task_size"]=np.log(d.predicted_time_no_ai)
    if not np.isfinite(d[["log_y","log_task_size"]].to_numpy()).all():
        raise ValueError("Nonfinite logged outcome/covariate")
    fe=smf.ols("log_y ~ ai_treatment + log_task_size + C(dev_id)",data=d).fit(
        cov_type="cluster",cov_kwds={"groups":d.dev_id},use_t=True)
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter("always")
        s6=smf.mixedlm("log_y ~ ai_treatment + log_task_size",data=d,
                       groups=d.dev_id).fit(reml=True,maxiter=200)
    s6warn=[str(x.message) for x in ww]
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter("always")
        s5=smf.mixedlm("log_y ~ ai_treatment + predicted_time_no_ai",data=d,
                       groups=d.dev_id).fit(reml=True,maxiter=200)
    s5warn=[str(x.message) for x in ww]
    models={"S1":summarize(fe,"Developer fixed effects / cluster robust t15"),
            "S2":summarize(fe,"Developer fixed effects / cluster robust t15"),
            "S6":summarize(s6,"Random intercept REML, log task size"),
            "S5_intended":summarize(s5,"Candidate intended random intercept REML, raw task size")}
    # A separate independent reconstruction of the LITERAL Patsy meaning of
    # the agent's written (1 | dev_id), not an execution of the agent script.
    # On integer developer IDs, Python bitwise-OR forms an unintended fixed
    # covariate in addition to the legitimate random intercept from groups.
    d["bitwise_or_developer"]=np.bitwise_or(1,d.dev_id.astype("int64"))
    try:
        with warnings.catch_warnings(record=True) as ww_literal:
            warnings.simplefilter("always")
            literal=smf.mixedlm(
                "log_y ~ ai_treatment + predicted_time_no_ai + bitwise_or_developer",
                data=d,groups=d.dev_id
            ).fit(reml=True,maxiter=200)
        lit=summarize(literal,"S5 literal Patsy bitwise OR covariate plus random intercept")
        lit["warnings"]=[str(w.message) for w in ww_literal]
        models["S5_literal_formula_analog"]=lit
    except Exception as exc:
        models["S5_literal_formula_analog"]={
            "status":"COULD_NOT_FIT","reason":type(exc).__name__+": "+str(exc)[:200]}
    models["S6"]["warnings"]=s6warn
    models["S5_intended"]["warnings"]=s5warn
    raw=json.loads((ROOT/"evaluation/heldout_v01_selected_claims.json").read_text())
    byid={c["claim_id"]:c for c in raw["claims"]}
    mapping={"S1-C3":("S1","gmr"),
             "S2-C3":("S2","percent_change"),
             "S5-C1":("S5_intended","percent_change"),
             "S5-C2":("S5_intended","ci_gmr"),
             "S5-C3":("S5_intended","p"),
             "S6-C1":("S6","percent_change"),
             "S6-C2":("S6","ci_gmr"),
             "S6-C3":("S6","p")}
    comparisons=[]
    for cid,(m,k) in mapping.items():
        comparisons.append({"claim_id":cid,"reported":byid[cid]["reported"],
          "recomputed":models[m][k],"model":m,"gold_label":None,
          "second_independent_reviewer":False,
          "interpretation":"MODEL_SPECIFICATION_UNRESOLVED" if cid.startswith("S5")
                            else "PRELIMINARY_SAME_SPECIFICATION_RECOMPUTATION"})
    return {"dataset_sha256":digest,"source_agent_code_executed":False,
      "statsmodels_version":statsmodels.__version__,"samples":len(d),
      "S5_formula_issue":"The released S5 Python formula contains (1 | dev_id). "
          "Patsy interprets this as a bitwise-or computed fixed-effect term, "
          "not R random-effect syntax. A separate groups argument already "
          "specifies a random intercept. We calculate the intended formula "
          "but do not assume it produced the reported values.",
      "models":models,"comparisons":comparisons}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--metr",type=Path,required=True)
    p.add_argument("--output",type=Path,default=Path("results/heldout_v01/metr_model_evidence.json"))
    a=p.parse_args()
    result=run(a.metr)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("HELDOUT_METR_INDEPENDENT",json.dumps(result),flush=True)

if __name__=="__main__":main()
