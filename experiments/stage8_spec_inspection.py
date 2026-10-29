"""Extract source-verified statistical method clues from published agent code, WITHOUT running it."""
from __future__ import annotations
import json
import re
from pathlib import Path
from experiments.stage8_multiagent_compare import PERSONAS,MODEL,DATASET,REPO,list_runs,file_pair

KEY=re.compile(r"(?i)(mixedlm|mixedlm\.|\.fit\(|smf\.ols|ols\(|cov_cluster|ttest_1samp|ttest_rel|ttest_ind|permutation|bootstrap|sample|developer|groupby|random|log_initial|log_total|cluster|missing|exclude|dropna|primary|dev_id|predict)",re.I)

def trim(text:str, n:int=150) -> str:
    return text.strip()[:n]

def main():
    rows=[]
    for persona in PERSONAS:
        for timestamp in list_runs(persona):
            base=f"experiment_data/workspaces/{persona}/{MODEL}/{DATASET}/{timestamp}"
            code,code_hash=file_pair(base+"/final_analysis.py")
            report,report_hash=file_pair(base+"/mirrored_report.txt")
            codes=code.splitlines()
            keylines=[{"line":i+1,"text":trim(line,220)} for i,line in enumerate(codes) if KEY.search(line)]
            # Early code often declares primary model; later sensitivity analyses may differ.
            row={"persona":persona,"timestamp":timestamp,
                "report_sha256":report_hash["sha256"],"code_sha256":code_hash["sha256"],
                "first_100_report_lines":[{"line":i+1,"text":trim(line,250)} for i,line in enumerate(report.splitlines()[:100]) if line.strip()][:65],
                "statistical_code_lines":keylines[:65],
                "interpretation":"Static code/source observation only. Numeric consistency not evaluated."}
            rows.append(row)
            print("=== REPORT",persona,timestamp,"===",flush=True)
            for x in row["first_100_report_lines"][:32]: print(f'REPORT L{x["line"]:03d}: {x["text"]}',flush=True)
            print("=== AGENT SCRIPT STATISTICAL LINES, NOT EXECUTED ===",flush=True)
            for x in keylines[:52]:print(f'CODE L{x["line"]:03d}: {x["text"]}',flush=True)
    out=Path("results/stage8_method_inspection.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"records":rows,"not_executed_ai_scripts":True,
                              "scientifically_verified_reporting_errors":0},indent=2)+"\n")
    print("METHOD_INSPECTION_COMPLETE",len(rows),flush=True)
if __name__ == "__main__":
    main()
