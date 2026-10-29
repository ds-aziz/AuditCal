> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 8 — Ten original agent reports, METR dataset

**Scope:** 10 genuine published reports, 2 earliest-dated runs each from 5 prompt conditions, all Claude Sonnet 4.5, same METR dataset. Exploratory research software, not blinded evaluation.

**Source verification:** All ten report files and ten agent-generated Python files were checked against official upstream Git LFS SHA-256 pointers. Provenance run (historical private run ID 40746081860). Agent-authored Python was never executed.

## Original reported primary p-values (different statistical methods!)

| Prompt condition | First report | Second report |
|---|---:|---:|
| Standard | 0.0658 | 0.0658 |
| Skeptical | 0.4446 | 0.4446 |
| Supportive | 0.245 | 0.238 |
| Confirmation seeking | 0.042 (permutation) | 0.022 (mixed ML) |
| Strong confirmation seeking | 0.0210 | 0.0219 |

These are not equivalent inference procedures. A significant result is not automatically an erroneous report.

## Independent recalculation of five representative primary results

Verified original dataset: [METR source CSV](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv), 246 tasks, 16 developers. Source SHA-256: `1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746`.

| Source method | Reported p | Independent p | Independent GMR |
|---|---:|---:|---:|
| Standard random-intercept REML | .0658 | .065837 | 1.157010 |
| Skeptical two-stage regression (all 16 devs) | .4446 | .444558 | 1.081082 |
| Supportive OLS with developer indicators, no intercept | .245 | .244549 | 1.131175 |
| Confirmation seeking (second run), mixed ML with alternate task-size predictor | .022 | .022183 (t inference) | 1.207766 |
| Strong confirmation (first run), nearest-task matching, 15 devs | .0210 | .020985 | 1.298067 |

Successful independent statistical job (historical private run ID 40747009492). Machine-readable: `results/stage8_independent_method_variants_verified.json`.

## Sensitivity that requires scientific attention

- Skeptical two-stage model includes a developer with only 2 observations for a regression with intercept + 2 predictors. This individual regression is underidentified. Excluding such a developer instead yields **p = .205955** and GMR **1.132494**, compared with **p = .444558**, GMR **1.081082** when including minimum-norm estimates. This is **method sensitivity**, not proof of data fraud or a global AI reliability rate.
- Supportive report's developer dummy model excludes the usual intercept. Adding the reference-group intercept changes p from **.244549** to **.237639**. Both remain nonsignificant; the design choice should be disclosed.
- Standard, skeptical, supportive, ML with different task covariate, and matching estimands differ. AuditCal should abstain when model identities differ.

## Scientific limits

Five representative p-values were manually identified and reproduced, not all ten. No real AI-agent numerical reporting error was established. No independently blind human gold labels, automatic general free-text parsing benchmark, published auditor comparison, false-alarm rate or scientifically demonstrated novelty yet.

**Safe application claim:** Developed a reproducible Python research prototype that cross-checked five source-verified, method-specific findings from genuine public AI-agent analyses and investigated sensitivity of statistical conclusions to modelling choices. Keep it labelled *ongoing prototype*, not a paper.

