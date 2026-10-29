"""Exploratory audit-ready inventory of real published AI-agent reports.

Downloads genuine report and code as UNTRUSTED TEXT, verifies original Git LFS
SHA256 metadata against the released official pointer, NEVER runs agent code,
and records candidate numbers without calling any statistical claim wrong.

Do not use this to estimate accuracy or academic novelty.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import time
from collections import Counter
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = "amazon-science/agentic-forking-path"
MODEL = "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0"
DATASET = "sample_metr"
PERSONAS = ("standard", "negative", "positive", "confirmation_seeking", "strong_confirmation_seeking")
LFS = re.compile(r"^version https://git-lfs.github.com/spec/v1\noid sha256:([a-f0-9]{64})\nsize (\d+)\n?$")
P = re.compile(r"(?i)(?<![a-z])p(?:[- ]?value)?\s*(?:[:=]|is)\s*([<>]?\s*0?\.\d+)")
MODEL_LINE = re.compile(r"(?i)\b(mixed effect|mixedlm|cluster.robust|ols regression|logistic regression|random intercept|random effect|permutation test|t.test|robust standard error|primary estimand)\b")

def get(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "Aziz-CSC2027-AuditCal-reproducibility"})
    last = None
    for _ in range(2):
        try:
            with urlopen(req, timeout=45) as response:
                return response.read(2000000)
        except Exception as ex:
            last = ex
            time.sleep(1)
    raise RuntimeError(f"Download failed: {url}: {last}")

def list_runs(persona: str) -> list[str]:
    prefix=f"experiment_data/workspaces/{persona}/{MODEL}/{DATASET}"
    url=f"https://api.github.com/repos/{REPO}/contents/{quote(prefix, safe='/')}"
    items=json.loads(get(url))
    return sorted(x["name"] for x in items if x["type"] == "dir")[:2]

def file_pair(relative: str) -> tuple[str,dict]:
    pointer=get(f"https://raw.githubusercontent.com/{REPO}/main/{quote(relative,safe='/')}")
    match=LFS.fullmatch(pointer.decode("utf-8"))
    if not match:
        raise ValueError("Official upstream file is not a well-formed LFS pointer")
    expected_sha, expected_bytes=match.group(1), int(match.group(2))
    data=get(f"https://media.githubusercontent.com/media/{REPO}/main/{quote(relative,safe='/')}")
    digest=hashlib.sha256(data).hexdigest()
    if digest != expected_sha or len(data) != expected_bytes:
        raise ValueError(f"Upstream integrity mismatch: {relative}")
    return data.decode("utf-8"), {"sha256": digest, "bytes":len(data), "integrity_verified":True}

def report_digest(text: str) -> dict:
    lines=text.splitlines()
    hits=[]
    for index,line in enumerate(lines,1):
        if MODEL_LINE.search(line):
            hits.append({"line": index,"snippet":line.strip()[:190]})
        if len(hits)>=12:
            break
    relevant = []
    for index,line in enumerate(lines,1):
        if "p-value" in line.lower() or "p value" in line.lower():
            relevant.append({"line":index, "snippet":line.strip()[:220]})
        if len(relevant)>=12:
            break
    return {"source_report_lines":len(lines),
            "model_and_estimand_mentions_to_review":hits,
            "reported_p_value_lines_to_review":relevant}

def run(output:Path) -> dict:
    all_runs=[]
    for persona in PERSONAS:
        for timestamp in list_runs(persona):
            base=f"experiment_data/workspaces/{persona}/{MODEL}/{DATASET}/{timestamp}"
            item={"persona":persona, "timestamp":timestamp,
                  "model_path":MODEL, "dataset_path":DATASET,
                  "selection":"first two lexically sorted runs per persona",
                  "source_directory":f"https://github.com/{REPO}/tree/main/{quote(base,safe='/')}"}
            try:
                rep,rmeta=file_pair(base+"/mirrored_report.txt")
                source_code,cmeta=file_pair(base+"/final_analysis.py")
                item["report"]=rmeta
                item["analysis_code"]=cmeta
                item["source_code_contains_mixedlm"]="MixedLM" in source_code or "mixedlm" in source_code.lower()
                item["source_code_contains_ols"]="ols(" in source_code.lower() or "OLS(" in source_code
                item.update(report_digest(rep))
                item["status"]="ORIGINAL_REPORT_AND_CODE_VERIFIED"
            except Exception as ex:
                item["status"]="NOT_VERIFIED"
                item["blocker"]=str(ex)
            all_runs.append(item)
            print(json.dumps({"persona":persona,"timestamp":timestamp,
                  "status":item["status"],
                  "p_value_lines":item.get("reported_p_value_lines_to_review",[])[:6],
                  "model_lines":item.get("model_and_estimand_mentions_to_review",[])[:5]}),flush=True)
    counts=Counter(v["status"] for v in all_runs)
    report={"provenance":"official Amazon Science LFS release",
        "selection":"two earliest timestamps in each of five persona folders, fixed prior to inspecting report text",
        "sample_label":"exploratory non-blinded, NOT held-out",
        "models":["Claude Sonnet 4.5"],
        "datasets":["METR"],
        "run_count":len(all_runs),"counts":dict(counts),
        "recomputed_validity_labels":0,
        "errors_verified":0,
        "comparison_claim":"not evaluated; source triage only",
        "runs":all_runs}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path("results/stage8_multiagent_inventory.json"))
    args=parser.parse_args()
    result=run(args.out)
    print("STAGE8_SUMMARY",json.dumps({k:result[k] for k in ("run_count","counts","errors_verified")}),flush=True)
    if result["counts"].get("ORIGINAL_REPORT_AND_CODE_VERIFIED",0)<10:
        raise SystemExit("Some original agent report files could not be verified")
