"""Public-source provenance check. No analysis models, AI scripts or private files.

Search official OSF public file APIs for the exact original Soccer CSV; if a
direct public file is available, verify actual downloaded bytes against the
already pinned Penn State educational copy. Fail closed on ambiguity.
"""
from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "osf_original_soccer_provenance.json"
EDU_EXPECTED_SHA = "6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"
EDU_URL = (
    "https://raw.githubusercontent.com/psu-psychology/"
    "psych-490-reproducibility-2024-fall/"
    "b35582ee3f2bb4ee2cc8986a0a878081fbad495d/"
    "src/surveys/csv/CrowdstormingDataJuly1st.csv"
)
FORKSCOPE_SHA_MANIFEST = (
    "https://raw.githubusercontent.com/TZstats-Columbia/ForkSCOPE/"
    "d55603c3b2e58205885aba1ddaf4738a9cf38679/"
    "data/raw/CHECKSUMS.txt"
)
FORKSCOPE_EXPECTED_PATH = "data/soccer/soccer_raw.csv"
OSF_NODES = ("c9mkx", "fv8c3")  # original study & separate public OSF reference
TARGET = "crowdstormingdatajuly1st.csv"
MAX_BYTES = 100_000_000


def get(url: str, max_bytes: int) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "CSC2027-AuditCal-reproducibility-check/0.1",
        "Accept": "application/json, text/csv, */*",
    })
    with urllib.request.urlopen(req, timeout=45) as response:
        blob = response.read(max_bytes + 1)
        if len(blob) > max_bytes:
            raise ValueError("download exceeds configured safe maximum")
        return blob


def short_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return "HTTP " + str(exc.code)
    return type(exc).__name__ + ": " + str(exc)[:180]


def walk_node(node: str) -> tuple[list[dict], list[dict]]:
    todo = [f"https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page%5Bsize%5D=100"]
    checked: set[str] = set()
    found: list[dict] = []
    errors: list[dict] = []
    while todo and len(checked) < 45:
        url = todo.pop(0)
        if url in checked:
            continue
        checked.add(url)
        try:
            obj = json.loads(get(url, 2_500_000))
        except Exception as e:
            errors.append({"url":url, "error":short_error(e)})
            continue
        for entry in obj.get("data",[]):
            a = entry.get("attributes") or {}
            name = str(a.get("name") or "")
            kind = a.get("kind")
            if name.casefold() == TARGET and kind == "file":
                found.append({
                    "node":node,"name":name,
                    "id":entry.get("id"),
                    "size":a.get("size"),
                    "hashes":a.get("extra",{}).get("hashes",{}),
                    "download":(entry.get("links") or {}).get("download")
                })
            if kind == "folder":
                sub = (entry.get("relationships") or {}).get("files",{})
                href = ((sub.get("links") or {}).get("related") or {}).get("href")
                if href:
                    todo.append(href)
        link = (obj.get("links") or {}).get("next")
        if link and link not in checked:
            todo.append(link)
    if todo:
        errors.append({"error":"folder traversal limit reached"})
    return found, errors


def main() -> None:
    out = {
        "scope":"OSF public original CrowdstormingDataJuly1st.csv versus pinned Penn State copy",
        "expected_teaching_sha256":EDU_EXPECTED_SHA,
        "osf_nodes_searched":list(OSF_NODES),
        "access_status":"NOT_YET_VERIFIED",
        "no_original_agent_script_executed":True,
        "contains_no_researcher_private_artifacts":True,
        "original_matches":[],
        "api_access_errors":[],
    }
    try:
        edu = get(EDU_URL, MAX_BYTES)
        digest = hashlib.sha256(edu).hexdigest()
        out["educational_copy_sha256"]=digest
        out["educational_copy_bytes"]=len(edu)
        if digest != EDU_EXPECTED_SHA:
            raise ValueError("the educational copy does not match previously pinned hash")
        # Independent study provenance check from a pinned, public raw-input
        # manifest; this corroborates OSF-origin claim but does NOT constitute
        # our own direct retrieval of the original OSF bytes.
        try:
            manifest_text = get(FORKSCOPE_SHA_MANIFEST, 1_000_000).decode("utf-8")
            rows = [
                ln.split()
                for ln in manifest_text.splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")
            ]
            entries = [x for x in rows if len(x) == 3 and x[2] == FORKSCOPE_EXPECTED_PATH]
            if len(entries) != 1:
                raise ValueError("one unambiguous soccer_raw.csv entry required")
            third_party_sha, third_party_size, _ = entries[0]
            out["forkscope_pinned_manifest_url"] = FORKSCOPE_SHA_MANIFEST
            out["forkscope_osf_origin_claim"] = "OSF node c9mkx as documented by ForkSCOPE"
            out["forkscope_recorded_sha256"] = third_party_sha
            out["forkscope_recorded_bytes"] = int(third_party_size)
            out["independent_manifest_corrob"] = (
                third_party_sha == digest and int(third_party_size) == len(edu)
            )
            out["independent_manifest_note"] = (
                "Confirms educational copy matches separately published "
                "OSF-claimed dataset checksum; not independent download from OSF."
            )
        except Exception as e:
            out["independent_manifest_corrob"] = False
            out["independent_manifest_error"] = short_error(e)
        for node in OSF_NODES:
            found, errs = walk_node(node)
            out["api_access_errors"].extend(errs)
            out["original_matches"].extend(found)
        if not out["original_matches"]:
            out["access_status"]="NO_EXACT_CSV_FOUND_OR_ACCESS_BLOCKED"
        elif len(out["original_matches"]) != 1:
            out["access_status"]="MULTIPLE_CANDIDATES_NEED_MANUAL_PROVENANCE_RESOLUTION"
        else:
            selected = out["original_matches"][0]
            if not selected.get("download"):
                out["access_status"]="ORIGINAL_FOUND_NO_PUBLIC_DOWNLOAD_LINK"
            else:
                try:
                    osf = get(selected["download"],MAX_BYTES)
                    sha = hashlib.sha256(osf).hexdigest()
                    out["osf_original_sha256"]=sha
                    out["osf_original_bytes"]=len(osf)
                    out["byte_identical"]=sha == EDU_EXPECTED_SHA and len(osf)==len(edu)
                    out["access_status"]=(
                        "ORIGINAL_BYTES_MATCH_EDUCATIONAL_COPY" if out["byte_identical"]
                        else "ORIGINAL_BYTES_DIFFER_FROM_EDUCATIONAL_COPY"
                    )
                except Exception as e:
                    out["access_status"]="ORIGINAL_DOWNLOAD_FAILED"
                    out["download_error"]=short_error(e)
    except Exception as e:
        out["access_status"]="EDUCATIONAL_COPY_OR_CRITICAL_CHECK_FAILED"
        out["critical_error"]=short_error(e)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    summary = {k:v for k,v in out.items() if k not in ("original_matches","api_access_errors")}
    print("OSF_SOURCE_PROVENANCE",json.dumps(summary),flush=True)
    print("OSF_MATCH_CANDIDATES",json.dumps(out["original_matches"]),flush=True)
    print("OSF_API_ERROR_COUNT",len(out["api_access_errors"]),flush=True)
    if out["access_status"] == "EDUCATIONAL_COPY_OR_CRITICAL_CHECK_FAILED":
        raise SystemExit("critical pinned teaching source verification failed")
    # OSF access failure is NOT a fake 'PASS'. Archive an explicit unresolved result.

if __name__=="__main__":
    main()
