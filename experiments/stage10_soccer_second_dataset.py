"""Cross-dataset pilot on original soccer red-card observations.

Only exploratory descriptive statistics, not a causal bias estimate or a
performance benchmark. Do not execute released AI-generated analysis scripts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

REPO="amazon-science/agentic-forking-path"
RELEASE="d489f03b143fcaa9befb8cc443594ff63ec61eaa"
DATA_COPY_REPO="psu-psychology/psych-490-reproducibility-2024-fall"
DATA_COPY_REV="b35582ee3f2bb4ee2cc8986a0a878081fbad495d"
DATA_COPY_PATH="src/surveys/csv/CrowdstormingDataJuly1st.csv"
RESEARCH_ORIGINAL="https://osf.io/fv8c3/"
FILES=[
  dict(model="Claude Sonnet 4.5",
       folder="bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0",
       timestamp="2025-11-12T17-10-55+0000",
       report_sha="c1a3f19d89c2d89c44609b49a24eac5f13727888586b1eee3876d2d268eb701e",
       code_sha="45b8cd3a3713369264cda6afef032cb220485e6b08bcf4f55608e28ce5c3f01c"),
  dict(model="Qwen3 235B",
       folder="bedrock_qwen.qwen3-235b-a22b-2507-v1_0",
       timestamp="2025-12-11T19-37-43+0000",
       report_sha="87fcf04ba62bf81eb93fcf17d6596e623df82be9cdb3dccb33180c1c3dba2b45",
       code_sha="47b82061dbc70f634a5a2f669d243bf3bd5d8fb1aa8ca4382c61de7826d109ca")
]
REPORT_PATTERN=re.compile(r"(?i)primary|risk difference|risk ratio|red card|odds ratio|skin tone|rate|p.value|p-value|sample size|N\s*=|covariat|confidence|hypothesis|conclusion|adjusted")
CODE_PATTERN=re.compile(r"(?i)read_csv|rater[12]|redCards|yellowReds|games|logit|glm|ols|cluster|weight|offset|regress|fit\(|risk|refNum|playerShort")

def get_text(release_path:str, sha:str) -> tuple[str,dict]:
    url=f"https://media.githubusercontent.com/media/{REPO}/{RELEASE}/{quote(release_path,safe='/')}"
    req=Request(url,headers={"User-Agent":"AuditCal-source-verification"})
    with urlopen(req,timeout=45) as response:
        b=response.read(1000000)
    actual=hashlib.sha256(b).hexdigest()
    if actual!=sha:
        raise ValueError(f"Official release SHA256 mismatch: {release_path}")
    return b.decode("utf-8"),{"sha256":actual,"byte_length":len(b),"sha256_verified":True}

def candidate_lines(text:str,pattern:re.Pattern,max_lines:int=35) -> list[dict]:
    return [{"line":i,"text":v.strip()[:220]}
            for i,v in enumerate(text.splitlines(),1) if pattern.search(v)][:max_lines]

def inspect_agent_reports():
    out=[]
    for one in FILES:
        base=("experiment_data/workspaces/standard/"+
              one["folder"]+"/sample_soccer/"+one["timestamp"])
        report,rmeta=get_text(base+"/mirrored_report.txt",one["report_sha"])
        code,cmeta=get_text(base+"/final_analysis.py",one["code_sha"])
        record={
           "model":one["model"],
           "report_source":f"https://github.com/{REPO}/tree/{RELEASE}/{quote(base,safe='/')}",
           "report":rmeta,"agent_script":cmeta,
           "report_claim_candidates":candidate_lines(report,REPORT_PATTERN),
           "code_model_clues":candidate_lines(code,CODE_PATTERN),
           "original_agent_python_executed":False,
           "scientifically_verified_claims":0
        }
        out.append(record)
        print("AGENT_REPORT",json.dumps({
            "model":one["model"],
            "hashes_verified":True,
            "reported_claim_clues":record["report_claim_candidates"][:16],
            "method_clues":record["code_model_clues"][:16]
        }),flush=True)
    return out

def summarize_soccer(path:Path):
    bs=path.read_bytes()
    frame=pd.read_csv(path,low_memory=False)
    expected={"playerShort","games","redCards","rater1","rater2","refNum"}
    if not expected.issubset(frame.columns):
        raise ValueError("Data schema mismatch: "+str(sorted(expected-set(frame.columns))))
    if len(frame)!=146028:
        raise ValueError(f"Expected published 146,028 dyads, saw {len(frame)}")
    df=frame.copy()
    for key in ("games","redCards","rater1","rater2"):
        df[key]=pd.to_numeric(df[key],errors="coerce")
    all_ratings=pd.concat([df["rater1"],df["rater2"]]).dropna()
    valid=df["games"].gt(0) & df["redCards"].ge(0)
    both_ratings=df["rater1"].notna() & df["rater2"].notna()
    sample=df[valid & both_ratings].copy()
    sample["skin_score"]=sample[["rater1","rater2"]].mean(axis=1)
    sample["any_red_card"]=sample["redCards"].gt(0)
    # Descriptive per dyad; does not account for games exposure, clustered
    # player/referee measurements, or confounders. Avoid a causal claim.
    descriptive={}
    for group, mask in [
        ("rating_below_or_at_midpoint",sample["skin_score"].le(0.5 if all_ratings.max()<=1 else 3)),
        ("rating_above_midpoint",sample["skin_score"].gt(0.5 if all_ratings.max()<=1 else 3))
    ]:
        part=sample.loc[mask]
        descriptive[group]={
            "dyads":int(len(part)),
            "positive_red_card_dyads":int(part["any_red_card"].sum()),
            "proportion_with_any_red_card":float(part["any_red_card"].mean()) if len(part) else None,
            "total_games_exposure":float(part["games"].sum()),
            "total_red_cards":float(part["redCards"].sum()),
            "red_cards_per_game":float(part["redCards"].sum()/part["games"].sum()) if part["games"].sum()>0 else None
        }
    return {
        "original_study_repository":RESEARCH_ORIGINAL,
        "source_copy_repository":f"https://github.com/{DATA_COPY_REPO}/blob/{DATA_COPY_REV}/{DATA_COPY_PATH}",
        "source_copy_sha256":hashlib.sha256(bs).hexdigest(),
        "original_osf_bytes_matched_directly":False,
        "copy_source_is_not_a_verified_original_OSF_byte_identical_file":True,
        "all_dyads":int(len(df)),
        "columns":list(df.columns),
        "unique_players":int(df["playerShort"].nunique()),
        "unique_referees":int(df["refNum"].nunique()),
        "missing_skin_rater_1":int(df["rater1"].isna().sum()),
        "missing_skin_rater_2":int(df["rater2"].isna().sum()),
        "valid_games_and_cards":int(valid.sum()),
        "valid_both_raters_and_exposure":int(len(sample)),
        "rater_min":float(all_ratings.min()),"rater_max":float(all_ratings.max()),
        "descriptive_groups_only":descriptive,
        "causal_skin_tone_bias_conclusion":"NOT EVALUATED",
        "report_statistical_claims_recomputed":0,
        "independent_blinded_annotations":0,
        "note":"Unadjusted exploratory association is not evidence of discriminatory behavior or a valid estimate of causal bias."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("datafile",type=Path)
    p.add_argument("--output",type=Path,default=Path("results/stage10_soccer_second_dataset.json"))
    a=p.parse_args()
    result={"new_dataset":"soccer referee–player interactions",
            "dataset":summarize_soccer(a.datafile),
            "agent_reports":inspect_agent_reports(),
            "evaluation_stage":"SOURCE_VERIFICATION_AND_DESCRIPTIVE_BASELINE_ONLY"}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("STAGE10_SUMMARY",json.dumps({
        "dataset_checksum":result["dataset"]["source_copy_sha256"],
        "n_dyads":result["dataset"]["all_dyads"],
        "valid_analytical_rows":result["dataset"]["valid_both_raters_and_exposure"],
        "descriptive":result["dataset"]["descriptive_groups_only"],
        "source_verified_agent_reports":len(result["agent_reports"]),
        "independently_recomputed_agent_claims":0,
        "errors_verified":0
    }),flush=True)

if __name__=="__main__":
    main()
