> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 9 — Cross-model reproducibility pilot on authentic AI-agent reports

**Project:** AuditCal statistical claim verification research prototype
**Date:** 2026-10-28
**Outcome:** six real published reports verified; six selected numerical claims independently calculated, with **five matching the stated decimal-place rounding and one requiring a minor precision review**.

## Upstream data and source-integrity checks

- Reports from the [Amazon Science Agentic Garden of Forking Paths repository](https://github.com/amazon-science/agentic-forking-path/tree/d489f03b143fcaa9befb8cc443594ff63ec61eaa/experiment_data/workspaces), revision `d489f03b143fcaa9befb8cc443594ff63ec61eaa`.
- Fixed selection before analysis: first two lexicographically sorted METR/standard-persona runs for each of three **additional model variants**: Claude Haiku 4.5, Qwen3 235B, and Qwen3 Coder 480B. The last two belong to the broader Qwen3 family; this is **three distinct models, not three unrelated model families**.
- For each of six runs, both `mirrored_report.txt` and `final_analysis.py` were downloaded and their SHA-256 compared with the official Git LFS pointer. All 12 original source files verified.
- Verification: GitHub workflow Stage 9 source check (historical private run ID 40748436242). The original AI-generated code was *read as text*, **never executed**.
- Independent source data: [official METR 2025 coding-time dataset](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv), fixed SHA-256 `1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746`, N=246, 16 developers.

## Independent primary statistical recomputation

Our independently authored script `experiments/stage9_crossmodel_metr_reanalysis.py` fits:

- **Standard model:** random-developer-intercept mixed model by REML, with `log(initial implementation time)` and `log(predicted time without AI)`. It obtains p = **0.06583731**, exponentiated coefficient = **1.15700955**.
- **Qwen3 Coder second-run variant:** random-developer-intercept mixed model by REML with `log(initial implementation time + 1)` and **arithmetic mean of two task-duration predictions as a raw covariate**. It obtains p = **0.11581278**, exponentiated coefficient = **1.13922057**.

| Original model and run | Reported p | Independent p | Precision status |
|---|---:|---:|---|
| Claude Haiku 4.5, run 1 | 0.0658 | 0.065837 | Matches 4 displayed decimals |
| Claude Haiku 4.5, run 2 | 0.067 | 0.065837 | **Precision / specification review needed** |
| Qwen3 235B, run 1 | 0.066 | 0.065837 | Matches 3 displayed decimals |
| Qwen3 235B, run 2 | 0.066 | 0.065837 | Matches 3 displayed decimals |
| Qwen3 Coder 480B, run 1 | 0.0658 | 0.065837 | Matches 4 displayed decimals |
| Qwen3 Coder 480B, run 2 | 0.1158 | 0.115813 | Matches 4 displayed decimals; different method |

The reported GMR estimates agree within the preregistered **pilot engineering** tolerance 0.003. **Six of six p-values agree within the initial lenient tolerance ±0.003; only five of six meet strict decimal-place rounding checks**. The Haiku second-run discrepancy of about 0.001163 is not the same as ordinary 3-decimal rounding; it is a potential reporting/fit difference for *manual review*, not a proven substantive statistical error. All these p-values exceed 0.05 and no significance decision changes.

## Two methodological issues worth reviewing

**Different target variable.** The Qwen3 Coder second-run model applies `log(minutes+1)`. Exponentiating the treatment coefficient gives a ratio associated with `minutes+1`, not literally the geometric mean ratio of unshifted minutes. It also adjusts for a different task-size predictor. Comparing its p = 0.1158 against another agent's 0.0658 without model alignment would create a false accusation; AuditCal must **abstain**.

**Narrative support versus significance.** The second Haiku report's executive summary says the hypothesis is **SUPPORTED**, even though its own primary p ≈ 0.067 and secondary p ≈ 0.051 are above 0.05. This raises a *decision-rule interpretation question*. Whether this is an error depends on the task's prior criterion for hypothesis support and the report's full framing; it is **not independently adjudicated**. This should become a human-reviewed test case, not an automatic error.

## Limits, relevance and next steps

- These are real released AI-agent analyses, but source selection, numerical-claim extraction and model association were **researcher-specified**; no blinded independent evaluation set or credible performance estimate exists.
- No original agent-produced scripts were executed. No independently labelled true scientific error has been confirmed.
- Do not claim research originality, publication, full statistical validity, or performance superiority over a baseline.
- Prior Stage 8 verified 10 Claude Sonnet 4.5 reports. Stage 9 expands to **16 source-verified reports across four distinct model variants**, all using the **same METR dataset**. Next evaluate another *dataset*, predefine correctness standards, and involve independent human annotation before publishing accuracy rates.

### Evidence

- Six authentic reports/scripts source verification (historical private run ID 40748436242)
- Independent cross-model statistical calculation (historical private run ID 40748913751)
- Machine-readable output: `results/stage9_other_models_verified_numeric_snapshot.json`.
- Validation tests: `tests/test_stage9_other_models_source_based.py`.

**Research summary:** "Built an ongoing reproducible Python research prototype that cross-checked statistical claims in original AI-agent reports across four model variants, using verified source files and independently calculated regression results, with explicit safeguards against invalid cross-model comparisons."
