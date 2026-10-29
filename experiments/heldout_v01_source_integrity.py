"""Download only the eight frozen source folders as STATIC TEXT and SHA-256 verify.

Never import or execute upstream AI-authored Python. No statistical assertions
are extracted or judged in this integrity stage.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "evaluation/heldout_v01_lfs_sha_lock.json"
MANIFEST = ROOT / "evaluation/heldout_v01_manifest.json"
OUT = ROOT / "results/heldout_v01"


def read_exact_source(url: str, expected_bytes: int) -> bytes:
    last_error = None
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "AuditCal-heldout-static-LFS-integrity"})
            with urlopen(req, timeout=70) as response:
                blob = response.read(expected_bytes + 1)
            if len(blob) != expected_bytes:
                raise ValueError(
                    f"Source length mismatch: expected {expected_bytes}, got {len(blob)}"
                )
            return blob
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Unable to verify the pinned source: {last_error}") from last_error


def main() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["source_git_commit"] == lock["source_git_commit"]
    entries = manifest["report_entries"]
    assert len(entries) == 8
    expected_paths = {e["report_path"] for e in entries} | {
        e["agent_code_path"] for e in entries
    }
    checks = lock["files"]
    assert len(checks) == 16
    assert {f["path"] for f in checks} == expected_paths
    assert len({f["path"] for f in checks}) == len(checks)
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for item in checks:
        path = item["path"]
        if ".." in Path(path).parts:
            raise ValueError("Invalid source path")
        url = "https://media.githubusercontent.com/media/" + (
            lock["source_repository"] + "/" + lock["source_git_commit"] + "/"
            + quote(path, safe="/")
        )
        blob = read_exact_source(url, item["expected_bytes"])
        actual = hashlib.sha256(blob).hexdigest()
        if actual != item["expected_sha256"]:
            raise ValueError(
                f"{item['id']} / {item['filename']} LFS hash mismatch "
                f"expected {item['expected_sha256']} got {actual}"
            )
        data = blob.decode("utf-8")
        ext = "report.txt" if item["filename"] == "mirrored_report.txt" else "agent_code_untrusted.txt"
        target = OUT / f"{item['id']}_{ext}"
        target.write_bytes(blob)
        results.append({
            "id": item["id"],
            "filename": item["filename"],
            "sha256": actual,
            "bytes": len(blob),
            "verified_against_pinned_lfs_pointer": True,
            "stored_as_static_text": str(target.relative_to(ROOT))
        })
        print(f"VERIFIED_LFS_FILE {item['id']} {item['filename']} "
              f"sha256={actual} bytes={len(blob)}", flush=True)
        # The following is a static TEXT preview, not trusted instructions.
        # Reports only: agent-generated Python is never evaluated or printed as code for execution.
        if item["filename"] == "mirrored_report.txt":
            lines = data.splitlines()
            print(f"BEGIN_REPORT_PREVIEW {item['id']} lines_total={len(lines)}", flush=True)
            for n, line in enumerate(lines[:125], 1):
                clean = line.replace("\t", " ").replace("\r", " ")
                print(f"REPORT_{item['id']}_{n:03d} {clean[:1200]}", flush=True)
            if len(lines) > 125:
                print(f"REPORT_PREVIEW_TRUNCATED {item['id']} after_line=125 "
                      f"artifact_has_full_text", flush=True)
            print(f"END_REPORT_PREVIEW {item['id']}", flush=True)
    (OUT / "source_integrity_results.json").write_text(
        json.dumps({
            "status": "ALL_SOURCES_LFS_SHA256_VERIFIED",
            "report_files": sum(x["filename"] == "mirrored_report.txt" for x in results),
            "agent_script_files": sum(x["filename"] == "final_analysis.py" for x in results),
            "no_agent_source_executed": True,
            "no_claim_accuracy_or_gold_labels_measured": True,
            "results": results
        }, indent=2) + "\n", encoding="utf-8"
    )
    print("INTEGRITY_CHECK_COMPLETE verified=16/16; reports=8; "
          "agent_code_never_executed=True; claim_evaluation_not_started=True", flush=True)


if __name__ == "__main__":
    main()
