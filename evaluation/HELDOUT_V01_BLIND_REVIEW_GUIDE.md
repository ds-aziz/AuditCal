# AuditCal v0.1 — Blind Independent Statistical Review Guide
**Created:** 2026-10-29
**Status:** Review requested/planned; **no external reviewer has yet responded or agreed**.
**Purpose:** Independent confirmation or disagreement on the six unresolved source-method claims from eight fixed real AI-agent research reports.

## Reviewer blinding and data integrity

Please do **not** open the researcher's numerical comparison/readout or previous AuditCal predictions until AFTER your first written source-based judgement is recorded. They are stored separately at evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md. You may use the upstream public report text, the original AI-produced script **as untrusted text only**, pinned source data and your own independently written statistical code.

**Do not execute original AI-authored scripts or assume their model choices are correct.** Re-implement calculations from the reported method and verify what the script actually specifies.

Upstream original report/script repository: amazon-science/agentic-forking-path, pinned Git commit d489f03b143fcaa9befb8cc443594ff63ec61eaa. Exact report paths and locked SHA256 files are recorded in heldout_v01_manifest.json and heldout_v01_lfs_sha_lock.json. All 16 original report/script files were downloaded and hash-verified in this successful source run (historical private CI run 40854338435; access restricted).

Official METR data repository: METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs, commit 7ff2d7670235f531dff77eff58355bd77392f396, data_complete.csv, SHA256 1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746.

Soccer data: Penn State teaching copy, repo psu-psychology/psych-490-reproducibility-2024-fall, commit b35582ee3f2bb4ee2cc8986a0a878081fbad495d, src/surveys/csv/CrowdstormingDataJuly1st.csv; SHA256 6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a. **Do not treat this as independently proven byte-identical to the original OSF data.**

## First review: exact six unresolved frozen claims

| Original claim ID | Released source report | Original text to independently evaluate |
|---|---|---|
| S5-C1 | Qwen METR, run 2025-12-11T22-29-20+0000 | Main initial implementation time change reported as **+10.9%** |
| S5-C2 | Same S5 | Primary GMR 95% CI reported **[0.941, 1.308]** |
| S5-C3 | Same S5 | Primary two-sided p-value **0.215** |
| S6-C2 | Qwen METR, run 2025-12-11T22-35-55+0000 | Primary GMR 95% CI **[0.990, 1.351]** |
| S8-C2 | Qwen Soccer, run 2025-12-11T22-21-05+0000 | Primary adjusted RD **0.0811 percentage points** |
| S8-C3 | Same S8 | Primary 95% CI **[-0.0002, 0.202] percentage points** |

Original published source report and analysis scripts are already hash locked. The 24 original selected claims are immutable. The six above were identified from a conservative preliminary independent source-based reanalysis. They are **NOT claimed to be proven errors**.

## Reviewer tasks (written evidence, not yes/no intuition)

1. Reproduce the applicable sample-size/filter from the pinned data, noting missingness and sample cardinality.
2. Identify the formula implied by the *text* and the executable semantics of the separate released source script (without running it), especially link function, dev-id handling, input transformations, covariance method, CI and the exact definition of the estimand.
3. Independently calculate the reported point estimate, interval or p-value using code you wrote yourself. Give numeric values at 8+ significant digits where appropriate and the statsmodels/R version, plus warnings/convergence.
4. Check whether each published number satisfies the **frozen** reporting-rounding rule in HELDOUT_V01_PROTOCOL.md. Do not loosen rounding after seeing mismatches.
5. For each claim, state one of: supported under identical method/sample; genuine discrepancy under identical method/sample; or unadjudicable because model/estimand/inference is ambiguous or source evidence insufficient. Supply reasoning and reference exact code/report lines.
6. Explicitly distinguish a reporting error, a software-specification mismatch, a legitimate alternate method, numerical/rounding precision and a causal scientific conclusion. Source-code/report mismatch does **not** automatically imply data fraud or invalid scientific conclusion.
7. Before reading researcher comparisons, write your signed/date-stamped individual judgement in the companion unfilled JSON template. If disagreements remain, record them and request a third reviewer; do not force consensus.

## Review not limited to six forever

This targeted six-claim methodological review resolves urgent ambiguity; a genuine full 24-claim independent gold evaluation requires also reviewing the remaining 18 selected claims **without viewing AuditCal predictions**. A second reviewer independently checking just these six is **not equivalent** to 24 double-adjudicated gold labels.

## Open review status

No reviewer has been recruited/approved, no review submitted and no independently adjudicated ground truth yet. Do not run/report final AuditCal accuracy, precision, recall, false positive rate or baseline superiority in the absence of honest labels and denominators.

**Research scope:** The initial investigation concerns the boundary between source-data numerical reproduction and credible statistical-method interpretation. This packet intentionally withholds the researcher's conclusions until independent assessment is recorded.