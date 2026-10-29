"""STATIC ONLY inspection of the remaining five frozen METR/Soccer analysis specs.

AI-authored source scripts are fetched and SHA256 verified, then printed as inert
text. We must NEVER import/execute any of those scripts.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/"evaluation/heldout_v01_lfs_sha_lock.json").read_text())
prefix="https://media.githubusercontent.com/media/"+lock["source_repository"]+"/"+lock["source_git_commit"]+"/"

for wanted in ("S1","S2","S4","S5","S6"):
    entry=next(f for f in lock["files"] if f["id"]==wanted and f["filename"]=="final_analysis.py")
    url=prefix+quote(entry["path"],safe="/")
    req=urllib.request.Request(url,headers={"User-Agent":"AuditCal-frozen-model-static-inspection"})
    with urllib.request.urlopen(req,timeout=70) as response:
        blob=response.read(entry["expected_bytes"]+1)
    sha=hashlib.sha256(blob).hexdigest()
    if len(blob)!=entry["expected_bytes"] or sha!=entry["expected_sha256"]:
        raise ValueError("Frozen source mismatch for "+wanted)
    lines=blob.decode("utf-8").splitlines()
    print("BEGIN_FROZEN_MODEL_TEXT",wanted,"hash",sha,"lines",len(lines),flush=True)
    for ix,line in enumerate(lines,1):
        print(f"STATIC_{wanted}_{ix:03d} {line[:600]}",flush=True)
    print("END_FROZEN_MODEL_TEXT",wanted,flush=True)
print("STATIC_MODEL_INSPECTION_DONE source_scripts_executed=False",flush=True)
