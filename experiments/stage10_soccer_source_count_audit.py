"""Source-backed count consistency audit for a REAL external AI-generated report.

This checks factual dataset counts, not discrimination, causal inference or
statistical significance. Original model-authored Python is never executed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from experiments.stage10_soccer_second_dataset import FILES, get_text

KNOWN_COPY_HASH = "6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"

def audit_original_report(dataset: Path):
    observed_sha=hashlib.sha256(dataset.read_bytes()).hexdigest()
    if observed_sha != KNOWN_COPY_HASH:
        raise ValueError("Input does not match the vetted second dataset copy")
    data=pd.read_csv(dataset, low_memory=False)
    if data.shape[0]!=146028:
        raise ValueError("Unexpected source dataset row count")
    n_players=data["playerShort"].nunique(dropna=True)
    n_refs=data["refNum"].nunique(dropna=True)
    # Independently implement the printed inclusion criteria of the
    # publicly released Qwen3 script as a separate calculation.
    cleaned=data.dropna(subset=["rater1", "rater2"]).copy()
    cleaned["mean_skin"]=(cleaned["rater1"]+cleaned["rater2"])/2
    cleaned["skin_binary"]=float("nan")
    cleaned.loc[cleaned["mean_skin"]<=0.25,"skin_binary"]=0
    cleaned.loc[cleaned["mean_skin"]>=0.75,"skin_binary"]=1
    cleaned["any_red"]=(cleaned["redCards"]>0).astype(int)
    needed=["skin_binary","any_red","position","height","weight",
            "leagueCountry","games","meanIAT","meanExp","playerShort"]
    retained=cleaned.dropna(subset=needed)
    n_retained=len(retained)
    players_retained=int(retained["playerShort"].nunique())
    refs_retained=int(retained["refNum"].nunique())
    qwen=next(x for x in FILES if x["model"]=="Qwen3 235B")
    base=("experiment_data/workspaces/standard/"+
          qwen["folder"]+"/sample_soccer/"+qwen["timestamp"])
    report,prov=get_text(base+"/mirrored_report.txt",qwen["report_sha"])
    code,cprov=get_text(base+"/final_analysis.py",qwen["code_sha"])
    # Require the exact released source to contain the advertised phrase.
    match=re.search(r"(?<![\d,])(\d[\d,]*)\s+unique\s+players\b",report,re.I)
    if not match:
        raise ValueError("Original report no longer contains a concrete unique-player count")
    reported=int(match.group(1).replace(",",""))
    line_no=report[:match.start()].count("\n")+1
    sample_match=re.search(r"([0-9,]+)[ ]+dyads[ ]*[(]from",report,re.I)
    claimed_sample=int(sample_match.group(1).replace(",","")) if sample_match else None
    records={
      "source_report_sha256":prov["sha256"],
      "source_agent_code_sha256":cprov["sha256"],
      "source_data_sha256":observed_sha,
      "source_data_repository":"psu-psychology/psych-490-reproducibility-2024-fall",
      "source_data_version":"b35582ee3f2bb4ee2cc8986a0a878081fbad495d",
      "official_study_original":"https://osf.io/fv8c3/",
      "original_osf_data_bytes_held_and_checked":False,
      "report_model":"Qwen3 235B",
      "report_statement_location":f"mirrored_report.txt line {line_no}",
      "reported_unique_players":reported,
      "reported_final_dyads":claimed_sample,
      "independent_reimplementation_of_reported_selection": {
        "retained_dyads":n_retained,
        "retained_unique_players":players_retained,
        "retained_unique_referees":refs_retained,
        "selection":"Nonmissing two ratings; mean rating <= 0.25 or >= 0.75; complete cases for ten listed model columns"
      },
      "reported_dyads_differ_from_reimplemented_selection":bool(claimed_sample is not None and claimed_sample != n_retained),
      "all_source_unique_player_ids":int(n_players),
      "all_source_unique_referee_ids":int(n_refs),
      "all_source_rows":int(len(data)),
      "reported_players_exceed_total_source_players":bool(reported>n_players),
      "interpretation":("INCONSISTENT_WITH_UNMODIFIED_SOURCE_DATA_COPY"
         if reported>n_players else "NO_IMPOSSIBILITY_FOUND"),
      "scope":"DATASET DISTINCT-COUNT AUDIT ONLY",
      "statistical_inference_errors_confirmed":0,
      "discrimination_inference_performed":False,
      "original_agent_python_executed":False,
      "human_review_required_before_publication":True,
      "recorded_report_excerpt":report[max(0,match.start()-110):match.end()+70].replace("\n"," "),
      "source_agent_code_first_90_lines_as_untrusted_text":[
          f"{i+1:03d}: {line}" for i,line in enumerate(code.splitlines()[:90])
      ]
    }
    return records

def main():
    p=argparse.ArgumentParser()
    p.add_argument("csv",type=Path)
    p.add_argument("--output",type=Path,default=Path("results/stage10_real_report_count_audit.json"))
    args=p.parse_args()
    outcome=audit_original_report(args.csv)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(outcome,indent=2)+"\n",encoding="utf-8")
    print("STAGE10_COUNT_AUDIT",json.dumps({
        key:outcome[key] for key in
        ("reported_unique_players","reported_final_dyads",
         "independent_reimplementation_of_reported_selection",
         "reported_dyads_differ_from_reimplemented_selection",
         "all_source_unique_player_ids",
         "all_source_unique_referee_ids","all_source_rows",
         "interpretation","report_statement_location","recorded_report_excerpt")
    }),flush=True)
    print("ORIGINAL_CODE_STATIC_INSPECTION_START",flush=True)
    for line in outcome["source_agent_code_first_90_lines_as_untrusted_text"]:
        print(line[:240],flush=True)
    print("ORIGINAL_CODE_STATIC_INSPECTION_END",flush=True)

if __name__=="__main__":
    main()
