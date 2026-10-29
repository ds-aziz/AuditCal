"""Independent same-specification Soccer model reanalysis for frozen claims.

Uses pinned educational copy. AI-written analysis scripts were inspected as
STATIC TEXT; none of their programs are imported or executed here.
No causal conclusions or gold reviewer labels follow from these fits.
"""
from __future__ import annotations
import argparse, hashlib, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT=Path(__file__).resolve().parents[1]
SHA="6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"

def groups(position):
    if pd.isna(position):return np.nan
    p=str(position).lower()
    if "goalkeeper" in p:return "Goalkeeper"
    if "back" in p or "fullback" in p:return "Defender"
    if "midfielder" in p:return "Midfielder"
    if "forward" in p or "winger" in p:return "Forward"
    return "Other"

def fit_s3(d):
    z=d.copy()
    z["tone"]=(z["rater1"]+z["rater2"])/2
    z["dark"]=(z["tone"]>=0.5).astype(float)
    z["any_red"]=(z["redCards"]>0).astype(int)
    z["pos_simple"]=z["position"].apply(groups)
    z["age_2013"]=2013-pd.to_datetime(z["birthday"],format="%d.%m.%Y",
                                             errors="coerce").dt.year
    keep=z["tone"].notna() & z[["height","weight","pos_simple","age_2013",
                                 "meanIAT","meanExp"]].notna().all(axis=1)
    z=z.loc[keep].copy()
    if len(z)!=115457:raise ValueError("S3 sample reconstruction changed")
    formula=("any_red ~ dark + games + C(pos_simple) + age_2013 + height + weight"
             " + C(leagueCountry) + meanIAT + meanExp")
    fit=smf.ols(formula,data=z).fit(cov_type="cluster",
                 cov_kwds={"groups":z["playerShort"]})
    est=float(fit.params["dark"])*100
    ci_wald=np.array([fit.params["dark"]-norm.ppf(.975)*fit.bse["dark"],
                      fit.params["dark"]+norm.ppf(.975)*fit.bse["dark"]])*100
    return {"n":len(z),"model":formula,"rd_pp":est,
            "rd_pp_ci":[float(x) for x in ci_wald],
            "p":float(fit.pvalues["dark"]),"method":"OLS LPM with player-cluster robust covariance",
            "converged":True}

def fit_s4(d):
    z=d.copy()
    z["tone"]=(z["rater1"]+z["rater2"])/2
    z["dark"]=np.nan
    z.loc[z["tone"]<=.25,"dark"]=0
    z.loc[z["tone"]>=.75,"dark"]=1
    z=z[z["dark"].notna() & z["position"].notna()].copy()
    z["any_red"]=(z.redCards>0).astype(int)
    for v in ("games","yellowCards","height"):
        z[v+"_std"]=(z[v]-z[v].mean())/z[v].std()
    clean=["dark","games_std","yellowCards_std","height_std",
           "position","leagueCountry","any_red","playerShort","refNum"]
    z=z.dropna(subset=clean).copy()
    form=("any_red ~ dark + games_std + yellowCards_std + height_std"
          " + C(position) + C(leagueCountry)")
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter("always")
        fit=smf.logit(form,data=z).fit(maxiter=100,disp=False,cov_type="cluster",
                           cov_kwds={"groups":z["playerShort"]})
    x=fit.model.exog.copy()
    idx=fit.model.exog_names.index("dark")
    x0=x.copy();x0[:,idx]=0
    x1=x.copy();x1[:,idx]=1
    beta=np.asarray(fit.params)
    p0=expit(x0@beta);p1=expit(x1@beta)
    rd_pp=float(np.mean(p1-p0))*100
    return {"n":len(z),"rd_pp":rd_pp,
            "odds_ratio":float(np.exp(beta[idx])),
            "method":"Player-clustered logit; discrete standardized 0-to-1 RD",
            "warnings":[str(w.message) for w in ww],
            "converged":bool(fit.mle_retvals.get("converged",False))}

def skin_contrast(d):
    mean=d[["rater1","rater2"]].mean(axis=1,skipna=True)
    return (mean<=.25)|(mean>=.75),mean

def fit_s7(d):
    good,mean=skin_contrast(d)
    z=d.loc[good & d[["height","weight"]].notna().all(axis=1)].copy()
    if len(z)!=106920:raise ValueError("S7 sample reconstruction changed")
    z["dark"]=(mean.loc[z.index]>=.75).astype(int)
    z["any_red"]=(z.redCards>0).astype(int)
    p=pd.get_dummies(z["position"],prefix="pos",drop_first=True,dtype=float)
    x=pd.concat([z[["dark","games","height","weight"]].astype(float),p],axis=1)
    x=sm.add_constant(x,has_constant="add")
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter("always")
        family=sm.families.Binomial(link=sm.families.links.Identity())
        fit=sm.GLM(z["any_red"].to_numpy(),x,family=family).fit(
            cov_type="cluster",cov_kwds={"groups":z["playerShort"].to_numpy()},
            maxiter=100)
    return {"n":len(z),"rd":float(fit.params["dark"]),
            "p":float(fit.pvalues["dark"]),
            "converged":bool(fit.converged),
            "warnings":[str(w.message) for w in ww],
            "method":"Binomial identity-link GLM / player-cluster covariance"}

def fit_s8(d):
    good,mean=skin_contrast(d)
    needed=["position","leagueCountry","height","weight","games",
            "redCards","playerShort","refNum"]
    z=d.loc[good & d[needed].notna().all(axis=1)].copy()
    if len(z)!=99645:raise ValueError("S8 sample reconstruction changed")
    z["dark"]=(mean.loc[z.index]>=.75).astype(int)
    yy=np.column_stack([z["redCards"],z["games"]-z["redCards"]])
    if (yy<0).any():raise ValueError("S8 invalid binomial trials")
    x=z[["dark","height","weight","position","leagueCountry"]].copy()
    x=sm.add_constant(x)
    x=pd.get_dummies(x,columns=["position","leagueCountry"],drop_first=True,dtype=float)
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter("always")
        fit=sm.GLM(yy,x.astype(float),family=sm.families.Binomial()).fit(
            cov_type="cluster",cov_kwds={"groups":z["playerShort"].to_numpy()},
            maxiter=100)
    beta=np.asarray(fit.params)
    v=np.asarray(fit.cov_params())
    ix=list(x.columns).index("dark")
    p=expit(x.to_numpy()@beta)
    der=float(np.mean(beta[ix]*p*(1-p)))
    grad=np.mean((beta[ix]*p*(1-p)*(1-2*p))[:,None]*x.to_numpy(),axis=0)
    grad[ix]+=float(np.mean(p*(1-p)))
    se=float(np.sqrt(grad@v@grad))
    ci=[float(100*(der+sgn*norm.ppf(.975)*se)) for sgn in (-1,1)]
    x0=x.to_numpy().copy();x0[:,ix]=0
    x1=x.to_numpy().copy();x1[:,ix]=1
    discrete=float(np.mean(expit(x1@beta)-expit(x0@beta)))
    return {"n":len(z),"derivative_rd_pp":100*der,"derivative_ci_pp":ci,
            "derivative_p":float(2*norm.sf(abs(der/se))),
            "discrete_rd_pp":100*discrete,
            "odds_ratio":float(np.exp(beta[ix])),
            "converged":bool(fit.converged),"warnings":[str(w.message) for w in ww],
            "method":"Binomial trials/logit cluster covariance; derivative AME delta method",
            "note":"Released code uses derivative marginal effect; report labels it as RD"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--soccer",type=Path,required=True)
    ap.add_argument("--output",type=Path,default=Path("results/heldout_v01/soccer_model_evidence.json"))
    args=ap.parse_args()
    with args.soccer.open("rb") as f:
        sha=hashlib.file_digest(f,"sha256").hexdigest()
    if sha!=SHA:raise ValueError("Soccer teaching-copy source SHA mismatch")
    d=pd.read_csv(args.soccer,low_memory=False)
    claims=json.loads((ROOT/"evaluation/heldout_v01_selected_claims.json").read_text())
    byid={c["claim_id"]:c for c in claims["claims"]}
    result={"source_sha256":sha,"statsmodels":statsmodels.__version__,
            "AI_source_code_executed":False,"second_reviewer":False,
            "reports":{},"claims":[]}
    for id,func in (("S3",fit_s3),("S4",fit_s4),("S7",fit_s7),("S8",fit_s8)):
        try:
            report=func(d)
            result["reports"][id]=report
            print("FROZEN_SOCCER_MODEL",id,json.dumps(report),flush=True)
        except Exception as exc:
            result["reports"][id]={"exception":type(exc).__name__,
                                   "error":str(exc)[:350],"verified":False}
            print("FROZEN_SOCCER_MODEL_UNRESOLVED",id,
                  type(exc).__name__,str(exc)[:350],flush=True)
    choices={"S3-C2":("S3","rd_pp"),"S3-C3":("S3","rd_pp_ci"),
             "S4-C3":("S4","rd_pp"),"S7-C3":("S7","rd"),
             "S8-C2":("S8","derivative_rd_pp"),"S8-C3":("S8","derivative_ci_pp")}
    for id,(model,field) in choices.items():
        row=result["reports"][model]
        result["claims"].append({"claim_id":id,"reported":byid[id]["reported"],
             "recomputed":row.get(field),"fit_available":field in row,
             "status":"PRELIMINARY_NUMERIC_NOT_GOLD" if field in row
                      else "UNRESOLVED_MODEL_REPRODUCTION",
             "gold_label":None,"second_human_review":False})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("FROZEN_SOCCER_REANALYSIS_COMPLETE",json.dumps(result["claims"]),flush=True)

if __name__=="__main__":main()
