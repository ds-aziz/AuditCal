> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 10 — Second research dataset obtained: soccer referee red-card data

**Date:** 29 October 2026 (Pakistan)
**Status:** Original public AI reports and a real second-domain CSV verified; this is **source provenance**, not independent numerical replication yet.

## Verifiable results

- Second dataset: Crowdstorming soccer referee dataset, from a [public research-course copy](https://github.com/psu-psychology/psych-490-reproducibility-2024-fall/tree/main/src/surveys/csv), associated with the published [Silberzahn et al. Many Analysts, One Data Set study](https://doi.org/10.1177/2515245917747646).
- CSV at `src/surveys/csv/CrowdstormingDataJuly1st.csv`: **146,028 rows**, **28 columns**, **33,305,306 bytes**; SHA-256 `6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a`. This verifies the downloaded public copy, **not equivalence with the original OSF file**.
- Real AI sources: two published Amazon Science **Claude Sonnet 4.5 / standard persona / sample_soccer** reports and their corresponding AI-authored scripts were retrieved and verified by matching official Git LFS SHA256 and size, not by trusting only filenames. Runs `2025-11-12T17-10-55+0000` and `2025-11-12T17-30-15+0000`.
- Successful Stage 10 GitHub workflow (historical private run ID 40752161744).
- Full reproducibility manifest: `results/stage10_soccer_source_verified_snapshot.json`.
- Neither released AI script was executed.

## What the two real reports say (NOT YET independently reproduced)

- First report: primary adjusted risk difference, p = **0.0200**; a **different adjusted odds-ratio analysis** says OR ~ **1.16**, p = **0.057** with cluster-robust standard errors. Their differing significance thresholds are not automatically a contradiction because the estimands and inference differ.
- Second report: adjusted risk difference approximately **0.27 percentage points**, p approximately **0.0158**. It also gives an odds ratio ~ **1.25** with p ~ **0.016**.
- These numbers are from original AI reports, **not AuditCal-verified results**. The public study concerns an observational dataset; no causal discrimination effect should be asserted merely from these numbers.

## Scientific next steps

1. Independently check whether this public CSV exactly matches the input used by the agent workspaces and the original OSF dataset. A matching shape alone is not enough.
2. Read the AI-produced model specifications, covariates, missing-data filters, cluster variance and bootstrap logic as *untrusted text*.
3. Design independent, minimal, non-AI-authored statistical implementations to reproduce the selected claims.
4. Label claims supported/flagged/unverifiable only with model alignment, and review uncertain issues with independent humans.
5. Report any differences transparently; do not claim scientific accuracy/novelty based only on GitHub tests.

**Research summary:** AuditCal is a reproducibility research-software prototype that has already replicated several real AI-agent results on METR and has now sourced and verified a second real-data domain for further evaluation. This stage alone does not demonstrate cross-dataset accuracy.

