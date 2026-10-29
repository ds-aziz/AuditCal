"""Source-verified sample from THREE NEW AI MODEL FAMILIES on the same METR data.

This script reads original agent reports and code as untrusted text.
It NEVER executes agent-written Python or calls a model.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = "amazon-science/agentic-forking-path"
REVISION = "d489f03b143fcaa9befb8cc443594ff63ec61eaa"
DATASET = "sample_metr"
PERSONA = "standard"
MODELS = {
    "Claude Haiku 4.5": (
        "bedrock_us.anthropic.claude-haiku-4-5-20251001-v1_0",
        ("2025-11-14T14-53-43+0000", "2025-11-14T15-33-39+0000")),
    "Qwen3 235B": (
        "bedrock_qwen.qwen3-235b-a22b-2507-v1_0",
        ("2025-12-11T22-20-15+0000", "2025-12-11T22-22-18+0000")),
    "Qwen3 Coder 480B": (
        "bedrock_qwen.qwen3-coder-480b-a35b-v1_0",
        ("2025-12-11T22-15-03+0000", "2025-12-11T22-17-28+0000"))
}
LFS_RE = re.compile(r"^version https://git-lfs.github.com/spec/v1\noid sha256:([a-f0-9]{64})\nsize (\d+)\n?$")
REPORT_LINE_RE = re.compile(
    r"(?i)primary|estimand|two-sided|p.value|confidence|significan|"
    r"mixed.effect|regress|t.test|sample size|N\s*=|geometric|"
    r"ratio|hypothesis|method|cluster|conclusion|initial implementation")
CODE_LINE_RE = re.compile(
    r"(?i)read_csv|mixedlm|smf\.ols|OLS\(|\.fit\(|ttest|permutation|bootstrap|"
    r"cov_cluster|log_initial|ai_treatment|predicted_time|formula|"
    r"cluster|groupby|dropna|pairwise|nearest")

def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "AuditCal-research-integrity-study"})
    with urlopen(request, timeout=35) as response:
        return response.read(1000000)

def authentic_text(relative_path: str) -> tuple[str,dict]:
    suffix = quote(relative_path, safe="/")
    raw = fetch(f"https://raw.githubusercontent.com/{REPO}/{REVISION}/{suffix}")
    m = LFS_RE.fullmatch(raw.decode("utf-8"))
    if not m:
        raise ValueError("Upstream release does not supply a recognizable LFS pointer")
    blob = fetch(f"https://media.githubusercontent.com/media/{REPO}/{REVISION}/{suffix}")
    sha = hashlib.sha256(blob).hexdigest()
    if sha != m.group(1) or len(blob) != int(m.group(2)):
        raise ValueError("Downloaded bytes do not match official upstream release")
    return blob.decode("utf-8"), {"sha256": sha, "bytes": len(blob), "source_hash_verified": True}

def snippets(source: str, pattern: re.Pattern, limit: int, max_line: int) -> list[dict]:
    output=[]
    for n,line in enumerate(source.splitlines(), 1):
        if n <= max_line and pattern.search(line):
            output.append({"line_number":n, "fragment": line.strip()[:180]})
        if len(output)>=limit:
            break
    return output

def collect() -> dict:
    records=[]
    for model_name,(folder,timestamps) in MODELS.items():
        for timestamp in timestamps:
            base=f"experiment_data/workspaces/{PERSONA}/{folder}/{DATASET}/{timestamp}"
            report, report_prov=authentic_text(base+"/mirrored_report.txt")
            code, code_prov=authentic_text(base+"/final_analysis.py")
            row={
                "model":model_name,"upstream_model_folder":folder,"persona":PERSONA,
                "timestamp":timestamp,"upstream_commit":REVISION,
                "source_dir":f"https://github.com/{REPO}/tree/{REVISION}/{quote(base,safe='/')}",
                "report":report_prov,"agent_script":code_prov,
                "report_line_candidates":snippets(report,REPORT_LINE_RE,30,145),
                "code_line_candidates":snippets(code,CODE_LINE_RE,28,170),
                "agent_code_executed":False,
                "interpretation":"Unreviewed snippets, not independent errors or certified model labels"
            }
            records.append(row)
            print(f"=== VERIFIED {model_name} {timestamp} ===",flush=True)
            print("SOURCE_BYTES",report_prov["bytes"],code_prov["bytes"],flush=True)
            print("REPORT HIGHLIGHTS:",flush=True)
            for item in row["report_line_candidates"][:25]:
                print(f'  {item["line_number"]}: {item["fragment"]}',flush=True)
            print("SOURCE CODE HIGHLIGHTS (never executed):",flush=True)
            for item in row["code_line_candidates"][:22]:
                print(f'  {item["line_number"]}: {item["fragment"]}',flush=True)
    data={
        "scope":"SOURCE TRIAGE ONLY; NOT A PERFORMANCE BENCHMARK",
        "selection":"Two lexicographically earliest run directories per distinct non-Sonnet model in the standard persona",
        "dataset":DATASET,"persona":PERSONA,
        "upstream_commit":REVISION,
        "unique_models":len(MODELS),
        "verified_report_and_script_pairs":len(records),
        "verified_statistical_errors":0,
        "independent_reanalyses_new":0,
        "original_ai_scripts_executed":0,
        "records":records
    }
    out=Path("results/stage9_other_models_source_inventory.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("STAGE9_INVENTORY",json.dumps({
        "models":data["unique_models"],
        "verified_report_and_script_pairs":len(records),
        "independent_reanalyses_new":0}),flush=True)
    return data

if __name__=="__main__":
    result=collect()
    assert result["verified_report_and_script_pairs"]==6
