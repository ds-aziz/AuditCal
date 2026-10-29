> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 11 — Independent Soccer Statistical Verification (two reports + previous count audit)

**Verified:** 29 October 2026 (Pakistan time)  
**Branch:** `auditcal-starter-v0-1`  
**Successful independent model + AuditCal audit:** historical private CI run 40754301086  
**Successful automated test run:** historical private CI run 40754301815

## Scope and provenance

- Two hash-verified **genuine Claude Sonnet 4.5** AI-agent reports from Amazon Science's public `agentic-forking-path` repository, on the soccer player–referee red-card dataset, were model-matched to independent Python analyses.
- Previous verified **Qwen3 235B** real-report count audit was included for cross-model context.
- Input is the pinned public **Penn State course copy** of Silberzahn et al.'s Crowdstorming soccer data: **146,028 rows, 28 columns**, SHA256 `6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a`.
- Equivalence to the original OSF hosted bytes has **not** been proven. Exact original AI report hashes are stored in the JSON result.
- The published AI source Python was **read as untrusted text and never executed**. Independent reconstruction uses a separately written GLM/patsy implementation, player-clustered standard errors, and independent marginal-effect calculations.
- Claim texts and model identities were mapped **manually**. This is *not* an autonomous natural-language claim-extraction test.

## Recomputed statistics

| Claim | Original published report | Independent estimate | Result |
|---|---:|---:|---|
| Claude 17:10 report sample N | 116,160 | 116,160 | Supported |
| Claude 17:10 dark/light dyads | 26,658 / 89,502 | 26,658 / 89,502 | Supported |
| Claude 17:10 red-card positive dyads | 1,457 | 1,457 | Supported |
| Claude 17:10 adjusted OR | 1.1574 | 1.1573936631 | Supported |
| Claude 17:10 cluster-robust OR CI | (0.9956, 1.3454) | (0.995646, 1.345418) | Supported |
| Claude 17:10 cluster-robust OR p | 0.0570 | 0.0570214 | Supported |
| Claude 17:30 report sample N | 107,606 | 107,606 | Supported |
| Claude 17:30 dark/light dyads | 17,490 / 90,116 | 17,490 / 90,116 | Supported |
| Claude 17:30 unique players/referees | 1,359 / 2,834 | 1,359 / 2,834 | Supported |
| Claude 17:30 red-card positive dyads | 1,344 | 1,344 | Supported |
| Claude 17:30 adjusted OR | 1.246 | 1.2462131101 | Supported |
| Claude 17:30 cluster-robust OR CI | (1.042, 1.490) | (1.042154, 1.490228) | Supported |
| Claude 17:30 cluster-robust OR p | 0.0158 | 0.0158427 | Supported |

The 17:10 report's point estimate for the **binary discrete g-computation risk difference** (0.1842 percentage points) independently reproduced as **0.1842383 percentage points**, but its **1,000-resample percentile bootstrap CI and bootstrap p-value were not rerun**. Delta-method p and CI must not be compared directly to bootstrap inference.

The 17:30 report states an RD of **0.27 percentage points** and p **0.0158**. Its released code invokes a **derivative average marginal effect** for a numeric binary regressor, whereas its narrative describes predicting under both exposure conditions (a **discrete contrast**). Recalculation gives:
- Derivative AME = **0.266560 percentage points**; cluster-delta p = **0.015794**.
- Discrete 0-to-1 standardized contrast = **0.285895 percentage points**; cluster-delta p = **0.023991**.
- This is a **method-definition/estimand alignment issue requiring adjudication**, **not a confirmed error in the AI's scientific conclusion**.

## Prior Qwen3 count audit incorporated

| Qwen3 reported claim | Independently reconstructed using its specified complete-case filters | AuditCal |
|---|---:|---|
| 99,535 analysis dyads | 99,535 | Supported |
| 9,959 unique players | 1,214 | Flagged discrepancy |
| 2,103 unique referees | 2,758 | Flagged discrepancy |

The entire original data copy has only 2,053 unique players, so 9,959 cannot be a unique-player count of a subset. That does not establish any model-estimate, causal, or fairness conclusion.

## Conservative AuditCal output (selected source-matched claims)

| Status | Number |
|---|---:|
| SUPPORTED | **17** |
| FLAGGED_DISCREPANCY | **2** |
| UNVERIFIABLE | **4** |
| **Total selected mapped claims** | **23** |

The four abstentions cover two unreproduced 17:10 bootstrap claims and two 17:30 risk-difference interpretation claims. The Qwen3 verified counts are from the **earlier** source-analysis snapshot; the two Claude regressions are freshly recomputed in this stage.

**These numbers are audit dispositions, not AuditCal precision, recall, or statistical accuracy.** The studies/reports were hand-selected, there is no blinded ground-truth panel, and false-positive/false-negative rates are unknown.

## Reproducible implementation

- `experiments/stage11_independent_soccer_models.py`: independent GLM, clustered covariance, discrete and derivative marginal-effect calculations and comparison output
- `experiments/stage11_audit_soccer_claims.py`: model-aligned structured claims sent through AuditCal core; abstains on missing or mismatched inferential definitions
- `src/auditcal/core.py`: extends supported claim kinds to strictly positive odds-ratio values
- `.github/workflows/stage11_soccer_independent_models.yml`: pinned source CSV acquisition, digest verification, model computation, AuditCal check, artifact upload
- `results/stage11_soccer_independent_models.json` and `results/stage11_soccer_auditcal_claims.json`: generated in successful Actions run and retained as workflow artifact, **not committed research input data**

## Next research work

1. Independently byte-verify the original OSF soccer data source against the pinned educational copy, or document access limitations.
2. Recompute the 17:10 bootstrap CI and p-value with a separately written, preregistered bootstrap design and replicate count.
3. Reproduce Qwen3 GEE identity-link risk difference and logit-link odds ratio; track convergence and clustering.
4. Ask an independent statistician to adjudicate the 17:30 report's derivative-versus-discrete contrast before calling it a reporting/method error.
5. Prespecify multi-model report sampling, human double-labeling, negative controls, baselines, audit precision/recall and abstention coverage. **Do not use selected-claim agreement as an out-of-sample reliability estimate.**

**Research summary:** AuditCal is a Python research-software prototype that has independently reconstructed source-matched numerical results from authentic AI-agent reports on METR and soccer datasets, identified reproducible count discrepancies, and deliberately abstained when inferential claims were not yet independently verified. No general performance benchmark or novel method is claimed.

