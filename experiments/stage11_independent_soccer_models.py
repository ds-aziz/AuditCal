"""Independent model recomputation for two published soccer reports.
Original AI-written scripts are never executed. Dataset is a pinned public course copy,
and identity with the study's original OSF data is not established.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
import patsy
import statsmodels.api as sm

SOURCE_HASH="6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"
CLAUDE_REPORTS={
 "claude_171055":"c1a3f19d89c2d89c44609b49a24eac5f13727888586b1eee3876d2d268eb701e",
 "claude_173015":"71ebb9fe572384a4db90e0c38705783f7f7aafe42a6dd8da249f4281ac3354fe"
}
def position_group(x):
    if pd.isna(x): return "Unknown"
    x=str(x)
    if "Forward" in x or "Winger" in x: return "Forward/Winger"
    if "Midfielder" in x: return "Midfielder"
    if "Back" in x or "Fullback" in x: return "Defender"
    if "Goalkeeper" in x: return "Goalkeeper"
    return "Other"

def make_sample(raw,key):
    if key=="claude_171055":
        data=raw[raw["tone"].notna() & raw["position"].notna()].copy()
        data["darkSkin"]=data.tone.ge(.5).astype(float)
        for c in ["height","weight"]:
            z=data[c].fillna(data[c].median())
            data[c+"_std"]=(z-z.mean())/z.std(ddof=1)
        formula="anyRedCard ~ darkSkin + log_games + height_std + weight_std + C(position) + C(leagueCountry)"
    else:
        data=raw[raw.tone.le(.25) | raw.tone.ge(.75)].copy()
        data["darkSkin"]=data.tone.ge(.75).astype(float)
        data["position_group"]=data.position.apply(position_group)
        formula="anyRedCard ~ darkSkin + log_games + C(position_group) + C(leagueCountry)"
    data["log_games"]=np.log(data.games)
    if not np.isfinite(data.log_games).all(): raise ValueError("Nonfinite game exposure")
    return data,formula

def compute(data,formula):
    outcome,design=patsy.dmatrices(formula,data,return_type="dataframe")
    if len(outcome)!=len(data): raise ValueError("Implicit model row exclusion")
    x=design.to_numpy()
    fit=sm.GLM(outcome.iloc[:,0].to_numpy(),x,family=sm.families.Binomial()).fit(
        cov_type="cluster",cov_kwds={"groups":pd.factorize(data.playerShort)[0]},
        maxiter=100,tol=1e-10)
    b=np.asarray(fit.params); v=np.asarray(fit.cov_params())
    idx=list(design.columns).index("darkSkin")
    se=np.sqrt(v[idx,idx]); zq=norm.ppf(.975)
    or_est=float(np.exp(b[idx]))
    or_ci=list(np.exp(b[idx]+np.array([-1,1])*zq*se))
    or_p=float(2*norm.sf(abs(b[idx]/se)))
    x0=x.copy(); x0[:,idx]=0
    x1=x.copy(); x1[:,idx]=1
    p0=expit(x0@b); p1=expit(x1@b)
    diff=float((p1-p0).mean())
    grad=np.mean((p1*(1-p1))[:,None]*x1-(p0*(1-p0))[:,None]*x0,axis=0)
    diff_se=np.sqrt(grad@v@grad)
    pm=expit(x@b)
    derivative=float(np.mean(b[idx]*pm*(1-pm)))
    gd=np.mean((b[idx]*pm*(1-pm)*(1-2*pm))[:,None]*x,axis=0)
    gd[idx]+=float(np.mean(pm*(1-pm)))
    der_se=np.sqrt(gd@v@gd)
    return {
     "n":len(data),"light_n":int((data.darkSkin==0).sum()),
     "dark_n":int((data.darkSkin==1).sum()),"events":int(data.anyRedCard.sum()),
     "unique_players":int(data.playerShort.nunique()),
     "unique_referees":int(data.refNum.nunique()),
     "light_events":int(data.loc[data.darkSkin.eq(0),"anyRedCard"].sum()),
     "dark_events":int(data.loc[data.darkSkin.eq(1),"anyRedCard"].sum()),
     "odds_ratio":or_est,"odds_ratio_ci":[float(q) for q in or_ci],
     "odds_ratio_cluster_p":or_p,
     "gcomp_binary_risk_difference":diff,
     "gcomp_delta_ci":[float(diff-s*diff_se) for s in (zq,-zq)],
     "gcomp_delta_p":float(2*norm.sf(abs(diff/diff_se))),
     "derivative_risk_difference":derivative,
     "derivative_delta_ci":[float(derivative-s*der_se) for s in (zq,-zq)],
     "derivative_delta_p":float(2*norm.sf(abs(derivative/der_se))),
     "method":"Independent GLM logistic with player-cluster covariance and delta method"
    }

def compare(key,output):
    published={
     "claude_171055":[("n",116160,0),("light_n",89502,0),("dark_n",26658,0),
        ("events",1457,0),("odds_ratio",1.1574,.00005),
        ("odds_ratio_cluster_p",.0570,.00005)],
     "claude_173015":[("n",107606,0),("light_n",90116,0),("dark_n",17490,0),
        ("unique_players",1359,0),("unique_referees",2834,0),
        ("events",1344,0),("odds_ratio",1.246,.0005),
        ("odds_ratio_cluster_p",.0158,.00005)]
    }
    check=[]
    for label,claim,tol in published[key]:
        measured=output[label]
        check.append(dict(claim=label,reported=claim,recomputed=measured,
                tolerance=tol,status="SUPPORTED" if abs(claim-measured)<=tol else "FLAGGED_DISCREPANCY"))
    if key=="claude_173015":
        check.append({"claim":"adjusted_risk_difference","reported":.0027,
          "recomputed_discrete":output["gcomp_binary_risk_difference"],
          "recomputed_derivative":output["derivative_risk_difference"],
          "status":"REQUIRES_ESTIMAND_REVIEW",
          "note":"Released script requests derivative AME; report describes a discrete risk contrast."})
    else:
        check.append({"claim":"bootstrap_risk_difference_ci_and_p",
                      "status":"UNVERIFIABLE","note":"1000 dyad-bootstrap draws not independently rerun."})
    return check

def main():
    src=Path("external_data/CrowdstormingDataJuly1st.csv")
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    if digest!=SOURCE_HASH: raise ValueError("Study-copy hash mismatch "+digest)
    data=pd.read_csv(src,low_memory=False)
    assert data.shape==(146028,28)
    data["tone"]=(data.rater1+data.rater2)/2
    data["anyRedCard"]=data.redCards.gt(0).astype(int)
    result={"data_copy_sha256":digest,"original_OSF_bytes_matched":False,
      "original_AI_code_executed":False,"original_AI_report_sha256":CLAUDE_REPORTS,
      "manually_specification_mapped":True,"causal_conclusions":False,"reports":{}}
    for key in CLAUDE_REPORTS:
        subset,formula=make_sample(data,key)
        numeric=compute(subset,formula)
        checks=compare(key,numeric)
        result["reports"][key]={"model_formula":formula,"independent":numeric,"checks":checks}
        print("SOCCER_MODEL",json.dumps({"key":key,"independent":numeric,"checks":checks}),flush=True)
    out=Path("results/stage11_soccer_independent_models.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("FINAL_STATUS",json.dumps({"output":str(out),"models_completed":len(result["reports"])}),flush=True)

if __name__=="__main__": main()
