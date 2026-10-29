"""Independent exploratory comparison of distinct methods described by real AI agents.

Uses primary released METR data; no AI-authored scripts executed. Comparing
different estimands is NOT a legitimate calculation-error accusation.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

def entry(beta, se, p, n, method, **extra):
    return dict(method=method, beta=float(beta), gmr=float(np.exp(beta)),
        p_value=float(p), se=float(se), N=int(n), **extra)

def cluster_fe(d, corrected):
    dummies=pd.get_dummies(d["dev_id"],prefix="dev",drop_first=True,dtype=float)
    X=pd.concat([d[["ai_treatment","log_pred_no_ai"]].reset_index(drop=True),
                 dummies.reset_index(drop=True)],axis=1).astype(float)
    if corrected:
        X=sm.add_constant(X,has_constant="add")
    fit=sm.OLS(d["log_time"].to_numpy(),X).fit(
        cov_type="cluster",cov_kwds={"groups":d["dev_id"],"use_correction":True})
    beta,se=float(fit.params["ai_treatment"]),float(fit.bse["ai_treatment"])
    p=2*stats.t.sf(abs(beta/se),d["dev_id"].nunique()-1)
    return entry(beta,se,p,len(d),
        ("FE + developer reference intercept + cluster robust" if corrected
         else "OLS with 15 developer indicators BUT NO INTERCEPT"),
        df=int(d["dev_id"].nunique()-1),num_parameters=len(fit.params))

def two_stage(d, include_small_sample=True):
    effects=[]
    for _,part in d.groupby("dev_id",sort=False):
        if part["ai_treatment"].nunique()!=2:
            continue
        x=np.column_stack([np.ones(len(part)),part["ai_treatment"],
                          part["log_pred_no_ai"]])
        if np.linalg.matrix_rank(x)<3 and not include_small_sample:
            continue
        X=part[["ai_treatment","log_pred_no_ai"]].to_numpy()
        y=part["log_time"].to_numpy()
        beta=np.linalg.lstsq(X-X.mean(axis=0),y-y.mean(),rcond=None)[0][0]
        effects.append(float(beta))
    t,p=stats.ttest_1samp(effects,0)
    beta=np.mean(effects);se=np.std(effects,ddof=1)/np.sqrt(len(effects))
    return entry(beta,se,p,len(d),"Two-stage equal-weight mean per-developer OLS treatment coefficient",
                 developers_with_effect=len(effects),t=float(t))

def matching(d):
    effects=[]
    skipped=[]
    for dev,part in d.groupby("dev_id",sort=False):
        treated=part[part["ai_treatment"]==1]
        control=part[part["ai_treatment"]==0]
        if len(treated)<2 or len(control)<2:
            skipped.append(str(dev))
            continue
        diffs=[]
        for _,task in treated.iterrows():
            match_index=(control["predicted_time_no_ai"]-task["predicted_time_no_ai"]).abs().idxmin()
            comparator=control.loc[match_index]
            diffs.append(float(np.log(task["initial_implementation_time"])-
                               np.log(comparator["initial_implementation_time"])))
        effects.append(float(np.mean(diffs)))
    t,p=stats.ttest_1samp(effects,0)
    beta=np.mean(effects);se=np.std(effects,ddof=1)/np.sqrt(len(effects))
    return entry(beta,se,p,len(d),"Within-developer nearest-predicted-task-time matching (with replacement) and t-test",
                 matched_developers=len(effects),skipped_developer_ids=skipped,t=float(t))

def analyse(dataset):
    b=dataset.read_bytes(); d=pd.read_csv(dataset)
    d["log_time"]=np.log(d["initial_implementation_time"])
    d["log_pred_no_ai"]=np.log(d["predicted_time_no_ai"])
    d["log_pred_ai"]=np.log(d["predicted_time_ai_allowed"])
    mixed=smf.mixedlm("log_time ~ ai_treatment + log_pred_no_ai",data=d,
                    groups=d["dev_id"]).fit(reml=True)
    mixed_ml_other=smf.mixedlm("log_time ~ ai_treatment + log_pred_ai",data=d,
                    groups=d["dev_id"]).fit(reml=False)
    standard=entry(mixed.params["ai_treatment"],mixed.bse["ai_treatment"],
                   mixed.pvalues["ai_treatment"],len(d),
                   "Mixed random developer intercept, REML, task size predicted without AI")
    conf=entry(mixed_ml_other.params["ai_treatment"],mixed_ml_other.bse["ai_treatment"],
               mixed_ml_other.pvalues["ai_treatment"],len(d),
               "Mixed random developer intercept, ML, task size predicted with AI",
               p_from_wald_normal=float(mixed_ml_other.pvalues["ai_treatment"]),
               p_using_task_level_t=float(2*stats.t.sf(abs(mixed_ml_other.params["ai_treatment"] /
                 mixed_ml_other.bse["ai_treatment"]), len(d)-4)))
    methods={
      "original_standard_mixed":standard,
      "negative_two_stage_as_reported":two_stage(d,True),
      "negative_two_stage_excluding_low_information":two_stage(d,False),
      "positive_claimed_FE_no_intercept":cluster_fe(d,False),
      "proper_developer_FE_with_intercept":cluster_fe(d,True),
      "confirmation_ML_other_covariate":conf,
      "strong_confirmation_nearest_matching":matching(d),
    }
    return {"data_source":"official METR study release, fixed commit 7ff2d7670",
            "dataset_sha256":hashlib.sha256(b).hexdigest(),
            "observations":len(d),"developers":int(d["dev_id"].nunique()),
            "analysis_type":"Independent implementation of method descriptions; not executing agents",
            "methods":methods,
            "scientific_interpretation":"Distinct covariates, weighting, samples and inference designs cannot be treated as identical estimands. Some implementation choices may require review; correctness needs design-specific assessment.",
            "not_benchmark":True}
def main():
    a=argparse.ArgumentParser()
    a.add_argument("csv",type=Path)
    a.add_argument("--out",type=Path,default=Path("results/stage8_independent_method_variants.json"))
    args=a.parse_args()
    result=analyse(args.csv)
    args.out.parent.mkdir(exist_ok=True,parents=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
