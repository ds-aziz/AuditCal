"""Protect the professor-facing research repository's essential navigation.

These tests exercise structure and links, NOT scientific accuracy.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")


def test_readme_distinguishes_completed_and_future_work():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "What our authentic-data investigations found" in readme
    assert "Proposed Master's research" in readme
    assert "not a demonstrated" in readme
    assert (ROOT / "docs/RESEARCH_ROADMAP.md").is_file()


def test_all_documentation_relative_links_point_to_existing_paths():
    paths = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")),
             *sorted((ROOT / "evaluation").glob("*.md")),
             *sorted((ROOT / "reproducibility").rglob("*.md"))]
    missing = []
    for doc in paths:
        for link in LINK.findall(doc.read_text(encoding="utf-8")):
            destination = link.split("#", 1)[0].split("?", 1)[0]
            if not destination or re.match(r"^(?:[a-z]+:|//)", destination, re.I):
                continue
            target = (doc.parent / destination).resolve()
            if not target.exists():
                missing.append(f"{doc.relative_to(ROOT)} -> {destination}")
    assert not missing, "Broken relative documentation links: " + "; ".join(missing)


def test_original_project_code_and_research_evidence_are_present():
    for name in ("src/auditcal/core.py",
                 "experiments/heldout_v01_s8_method_diagnostic.py",
                 "experiments/stage9_crossmodel_metr_reanalysis.py",
                 "evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md",
                 "docs/RESEARCH_HISTORY_INDEX.md",
                 "docs/THIRD_PARTY_SOURCES.md"):
        assert (ROOT / name).is_file()
    assert not (ROOT / "scholarship").exists()
    assert not (ROOT / "MASTER_PROJECT_STATE.md").exists()
