> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 5: genuine-agent record acquisition and source triage

## Real source found

The official Amazon Science [agentic-forking-path experiment data](https://github.com/amazon-science/agentic-forking-path/tree/main/experiment_data) README states **4,196 AI-agent-run workspaces**; this count is **reported by upstream authors, not independently counted here**. Each workspace may contain original AI report `mirrored_report.txt`, script `final_analysis.py`, and transcript `transcript.json`.

### What we could retrieve

A specific real source file exists at:

`experiment_data/workspaces/standard/bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/sample_metr/2025-11-12T17-17-32+0000/mirrored_report.txt`

The GitHub Contents API returned a **Git LFS pointer**, NOT the report itself:
- LFS SHA-256: `232c188e9aa155dee0056d79e115e065b85590b67be3972bb1dcae39dca2af23`
- Underlying reported size: **16,521 bytes**
- Report actual text downloaded: **NO**
- Genuine AI-report conclusions scored: **ZERO**

The new importer detects and rejects LFS pointers; it never executes AI-authored code. It can scan locally downloaded real reports, record hashes and model/persona labels inferred only from paths, and extract *unverified* p-value/coefficient mentions for subsequent manual annotation. It NEVER scores extracted numbers as errors on its own.

### Obtaining the actual reports

This GitHub project cannot currently fetch Git LFS objects via the read-only connector; a separate researcher may download selected actual LFS objects using Git LFS on an internet-enabled machine.

For example, with Git + Git LFS installed:
```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --filter=blob:none --sparse https://github.com/amazon-science/agentic-forking-path.git
cd agentic-forking-path
git sparse-checkout set experiment_data/workspaces/standard/bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/sample_metr/2025-11-12T17-17-32+0000
git lfs pull -I 'experiment_data/workspaces/standard/bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/sample_metr/2025-11-12T17-17-32+0000/mirrored_report.txt'
```
The above commands are proposed download instructions, not claimed executed here. The full dataset is large; start with one report.

To inspect downloaded reports locally, from the AuditCal repository root:
```bash
python -m experiments.ingest_published_agent_reports /path/to/agentic-forking-path/experiment_data/workspaces --limit 10
```

### Tests and scientific honesty

Seven new self-authored tests cover LFS pointer rejection, empty/unreadable files, cautious number mention extraction, and path metadata. Locally **32 tests passed** after addition (25 existing, 7 new). This is software testing, not benchmark success.

- Genuine AI agent reports evaluated: **0**
- Independently verified statistical errors: **0**
- Valid scientific performance or novelty claims: **NONE YET**

Next: acquire real LFS text + original analysis code + matching dataset, independently annotate model-aligned conclusions, preregister evaluation, then compare baselines. Do not claim a validated agent benchmark.
