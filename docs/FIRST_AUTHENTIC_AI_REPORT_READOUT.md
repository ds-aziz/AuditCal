> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 6 — first released AI-agent report obtained and hash-verified

**Repository:** [The Agentic Garden of Forking Paths (Amazon Science)](https://github.com/amazon-science/agentic-forking-path)

**Actual GitHub CI execution:** source-acquisition workflow run (historical private run ID 40743603764), result **success**.

## Verified progress (2026-10-28)

- One public release's `mirrored_report.txt` was downloaded **as actual 16,521-byte text**, not a Git LFS pointer.
- Its SHA-256 `232c188e9aa155dee0056d79e115e065b85590b67be3972bb1dcae39dca2af23` matches the upstream public LFS pointer.
- Source-path metadata suggests Claude Sonnet 4.5, standard persona, sample_metr dataset, timestamp `2025-11-12T17-17-32+0000`. Path metadata is **not** proof of model identity.
- AuditCal's conservative extraction identified **two unverified p-value mentions** and **zero coefficient mentions** using simple regular expressions.
- **Zero** numerical results from that report were recomputed against the actual dataset, so **zero** genuine AI statistical errors have been independently validated.
- Independently, GitHub Python tests (historical private run ID 40743603623) passed **32/32**. Those are self-authored engineering checks, not scientific benchmark measures.

## Next scientifically required steps

1. Independently obtain upstream `final_analysis.py` for exactly this run, inspect it as untrusted text only (do not execute AI-authored script).
2. Obtain input dataset and ground the model specification, sample exclusions, outcome definition, test choice, and standard-error method.
3. Recompute p-values in a controlled, human-reviewed implementation, preserving valid alternative analytical choices.
4. Independently annotate the validity of extracted claims; use blinded labels and distinct development/evaluation runs.
5. Compare against explicit baselines and report false-positive and abstention rates.

**Avoid claiming:** “AuditCal validated AI agent results,” “caught real agent errors,” “scientifically original system,” or “outperformed existing methods.”

**Accurate research summary:** “Developed a reproducible Python prototype to compare structured statistical claims against model-aligned evidence; implemented automated tests and source-integrity checks on a publicly released AI-agent report.”

Source and result metadata: `results/first_authentic_report_source_validation.json`.
