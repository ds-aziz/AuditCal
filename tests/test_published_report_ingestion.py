from experiments.ingest_published_agent_reports import inspect_report, ingest, extract_candidates

P = "workspaces/standard/bedrock_test/sample_metr/2025-11-12T17-17-32+0000"

def test_recognizes_lfs_pointer(tmp_path):
    folder = tmp_path / P
    folder.mkdir(parents=True)
    pointer = "version https://git-lfs.github.com/spec/v1\noid sha256:" + "a"*64 + "\nsize 16521\n"
    f = folder / "mirrored_report.txt"
    f.write_text(pointer)
    row = inspect_report(f, tmp_path)
    assert row["status"] == "LFS_POINTER_NOT_AGENT_TEXT"
    assert row["expected_lfs_bytes"] == 16521
    assert row["expected_lfs_sha256"] == "a"*64
    assert row["candidates"] == []
    assert row["attribution"] == "PATH_INFERRED_NOT_AUTHENTICATED"
    assert row["persona"] == "standard"
    rows, summary = ingest(tmp_path)
    assert summary["total_report_paths_scanned"] == 1
    assert summary["confirmed_authenticated_AI_traces"] == 0
    assert summary["independently_verified_AI_statistical_errors"] == 0

def test_extraction_not_scoring(tmp_path):
    folder = tmp_path / P
    folder.mkdir(parents=True)
    f = folder / "mirrored_report.txt"
    f.write_text("Coefficient: -0.23; p-value: 0.041. Another p-value < 0.001.\n")
    row = inspect_report(f, tmp_path)
    assert row["status"] == "TEXT_AVAILABLE_NOT_AUTHENTICATED"
    assert len(row["candidates"]) == 3
    assert sorted(c["kind"] for c in row["candidates"]) == ["coefficient","p_value","p_value"]
    assert all(c["validation_status"] == "REQUIRES_HUMAN_REVIEW" for c in row["candidates"])
    assert all(c["scientific_evidence"] is None for c in row["candidates"])
    assert "<" in [c["operator"] for c in row["candidates"]]

def test_empty_and_unreadable(tmp_path):
    folder = tmp_path / P
    folder.mkdir(parents=True)
    f = folder / "mirrored_report.txt"
    f.write_text("")
    assert inspect_report(f, tmp_path)["status"] == "EMPTY_TEXT"
    f.write_bytes(b"\xff\xfe\xfa")
    assert inspect_report(f, tmp_path)["status"] == "UNREADABLE_TEXT"

def test_unverified_path(tmp_path):
    f = tmp_path / "mirrored_report.txt"
    f.write_text("p-value=0.022")
    row = inspect_report(f, tmp_path)
    assert row["attribution"] == "UNVERIFIED_PATH"
    assert row["candidates"][0]["reported_number"] == 0.022

def test_empty_folder(tmp_path):
    records, summary = ingest(tmp_path)
    assert records == []
    assert summary["total_report_paths_scanned"] == 0

def test_reject_limit(tmp_path):
    try:
        ingest(tmp_path, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("limit=0 should be rejected")

def test_false_match_exclusion():
    assert extract_candidates("p-value: 4.3 and a coefficient=abc", "xyz") == []
