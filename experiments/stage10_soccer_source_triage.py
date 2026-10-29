"""Verify second, independent data domain for AuditCal: soccer referee bias.

Downloads two real published AI reports and AI-authored scripts, checks the
exact upstream LFS source hashes and file sizes, and reads their text without
executing any untrusted script. Also verifies public soccer dataset metadata.
"""
from __future__ import annotations
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT="amazon-science/agentic-forking-path"
MODEL="bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0"
DATA="sample_soccer"
TIMESTAMPS=("2025-11-12T17-10-55+0000","2025-11-12T17-30-15+0000")
MANIFEST={
    TIMESTAMPS[0]:{
        "mirrored_report.txt":("c1a3f19d89c2d89c44609b49a24eac5f13727888586b1eee3876d2d268eb701e",11335),
        "final_analysis.py":("45b8cd3a3713369264cda6afef032cb220485e6b08bcf4f55608e28ce5c3f01c",14131)},
    TIMESTAMPS[1]:{
        "mirrored_report.txt":("71ebb9fe572384a4db90e0c38705783f7f7aafe42a6dd8da249f4281ac3354fe",12813),
        "final_analysis.py":("f20b9373e2e3b05760ceb6401f7ff356898907874b65b1664fa4326dbcd9bf9f",2914)},
}
DATA_URL=("https://raw.githubusercontent.com/psu-psychology/"
          "psych-490-reproducibility-2024-fall/main/"
          "src/surveys/csv/CrowdstormingDataJuly1st.csv")
SOURCE_PAPER="https://doi.org/10.1177/2515245917747646"
LFS=re.compile(r"^version https://git-lfs.github.com/spec/v1\noid sha256:([a-f0-9]{64})\nsize (\d+)\n?$")
HIGHLIGHT=re.compile(r"(?i)primary|p.value|estimand|odds ratio|confidence|regression|logistic|skin|red card|model|significan")

def fetch(url, limit=80_000_000):
    req=urllib.request.Request(url,headers={"User-Agent":"AuditCal-independent-replication"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data=response.read(limit+1)
    if len(data)>limit: raise ValueError("Unexpected size")
    return data

def verify(path,expected):
    key=quote(path,safe="/")
    pointer=fetch(f"https://raw.githubusercontent.com/{ROOT}/main/{key}",10000).decode()
    pm=LFS.fullmatch(pointer)
    if not pm: raise ValueError("Not original Git LFS release pointer")
    assert (pm.group(1),int(pm.group(2)))==expected,"Upstream release changed"
    b=fetch(f"https://media.githubusercontent.com/media/{ROOT}/main/{key}",1_000_000)
    sha=hashlib.sha256(b).hexdigest()
    assert (sha,len(b))==expected,"Source integrity mismatch"
    return b.decode("utf-8"),{"sha256":sha,"bytes":len(b),"hash_checked":True}

def main():
    records=[]
    for timestamp in TIMESTAMPS:
        base=f"experiment_data/workspaces/standard/{MODEL}/{DATA}/{timestamp}"
        text,rep=verify(base+"/mirrored_report.txt",MANIFEST[timestamp]["mirrored_report.txt"])
        source,code=verify(base+"/final_analysis.py",MANIFEST[timestamp]["final_analysis.py"])
        selection=[]
        for i,line in enumerate(text.splitlines(),1):
            if HIGHLIGHT.search(line) and len(selection)<25:
                selection.append({"line":i,"text":line.strip()[:180]})
        report={
            "source":f"https://github.com/{ROOT}/tree/main/{quote(base,safe='/')}",
            "timestamp":timestamp,"persona":"standard","model":MODEL,
            "report":rep,"agent_code":code,
            "report_excerpts_for_manual_review":selection,
            "agent_code_was_executed":False,
            "numeric_claims_verified":0
        }
        records.append(report)
        print(f"ORIGINAL_SOCCER_REPORT_VERIFIED {timestamp}",flush=True)
        for item in selection[:18]:
            print(f"REPORT_L{item['line']}: {item['text']}",flush=True)
    downloaded=fetch(DATA_URL)
    if downloaded.startswith(b"version https://git-lfs.github.com/"):
        raise ValueError("Public soccer dataset is only an LFS pointer")
    if len(downloaded)<2_000_000:raise ValueError("Unusually small dataset")
    import csv,io
    line_count=sum(1 for _ in io.BytesIO(downloaded))-1
    header=next(csv.reader(io.StringIO(downloaded[:10000].decode("utf-8-sig").splitlines()[0])))
    dataset={"source_url":DATA_URL,
             "published_paper":SOURCE_PAPER,
             "bytes":len(downloaded),
             "sha256":hashlib.sha256(downloaded).hexdigest(),
             "row_count":line_count,
             "column_count":len(header),"columns":header,
             "note":"Public course copy; equivalence to upstream OSF original must still be independently verified"}
    result={"stage":"STAGE10_SECOND_DATASET_SOURCE_TRIAGE","new_domain":"soccer_red_cards",
            "original_real_ai_reports_hash_verified":2,
            "datasets_downloaded":1,
            "independent_model_recomputations":0,
            "scientifically_confirmed_AI_errors":0,
            "provenance_notes":"Original reports and code verified against public upstream LFS. Agent code not executed.",
            "dataset":dataset,"reports":records}
    p=Path("results/stage10_soccer_provenance.json")
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+"\n")
    print("STAGE10_RESULT_JSON",json.dumps(result,separators=(",",":")),flush=True)
if __name__=="__main__":main()
