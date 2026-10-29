> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 7 — independent numeric reproduction of authentic AI-agent report

**Verified on:** 2026-10-28
**Project:** AuditCal research software pilot
**Evidence report:** GitHub Actions independent reanalysis (historical private run ID 40744536806) (SUCCESS)
**Evidence auditor:** GitHub Actions authentic claim checking (historical private run ID 40744836252) (SUCCESS)

## Independently verified sources

1. The **real original published agent report**, in `amazon-science/agentic-forking-path`, model path consistent with Claude Sonnet 4.5, dataset `sample_metr`, run `2025-11-12T17-17-32+0000`.
2. Original report **SHA-256**: `232c188e9aa155dee0056d79e115e065b85590b67be3972bb1dcae39dca2af23`; report length **16,521 bytes**. Verified against upstream Git LFS pointer in source download job (historical private run ID 40743603764).
3. The released agent's `final_analysis.py` and `transcript.json` were also downloaded and source hashes checked in static inspection job (historical private run ID 40744192748). **No AI-authored code was executed.**
4. The source input dataset comes directly from the official [METR first-release 2025 RCT repository](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv), public snapshot commit `7ff2d7670235f531dff77eff58355bd77392f396`. **246 rows**, **16 developers**; downloaded CSV SHA-256 `1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746`.

## Original report vs truly independent Python recalculation

The following figures were obtained by **our separate, newly written** `experiments/independent_metr_reanalysis.py`. Its statistical equations match the source report's stated analysis but the AI's original `final_analysis.py` was not executed.

| Quantity | Original AI report | Independent recomputation | Status |
|---|---:|---:|---|
| Primary N | 246 | 246 | matches |
| Primary GMR (geometric mean ratio) | 1.1570 | 1.1570095502 | matches |
| Primary p-value | 0.0658 | 0.0658373111 | matches |
| Primary 95% CI (% time difference) | [-0.95, 35.15] | [-0.9502642, 35.1514054] | matches rounding |
| Secondary N | 230 | 230 | matches |
| Secondary GMR | 1.201 | 1.2011509345 | matches |
| Secondary p-value | 0.0382 | 0.0381530372 | matches |
| Secondary 95% CI (% time difference) | [1.15, 42.64] | [1.1488037, 42.6377293] | matches rounding |

**Primary model:** random-intercept mixed-effects model, REML, outcome log(initial implementation time), predictors AI treatment and log(pre-treatment predicted task time), developer random intercept, Wald normal p-value.

**Secondary model:** OLS on log(initial + post-review time), developer-clustered sandwich SEs, t inference with 15 degrees of freedom, complete-case N=230.

**Software actually used in CI:** statsmodels 0.14.6, pandas 3.1.0.

## Real claim audit

`experiments/audit_authentic_metr_claims.py` maps **8 reported numerical facts manually** to the matching independently computed model output:

- Primary: p-value, sample size, significance at 0.05, and confidence interval.
- Secondary: same four claims.

**Result: 8 supported / 0 discrepancies / 0 unverifiable.** The claim mapping was done manually, not auto-extracted; this is NOT a benchmark for automated natural-language understanding.

## What we can conclude

- One authentic externally produced AI analysis can be processed with a reproducible, source-verified, independently recomputed AuditCal evaluation.
- The *two selected estimands and eight mapped numerical claims* from this report are consistent with the independently computed results and their corresponding source data/model.
- **We did NOT detect a statistical reporting error in this report.** It is important not to manufacture a finding.

## What we CANNOT conclude

- NOT proven that the report's causal interpretation, random-effects assumptions, missing-data assumptions, or choice of estimand is substantively correct.
- NOT proven that the AI performed an unbiased selection of analysis choices; independent multiverse analysis remains future work.
- NOT proven that AuditCal is more accurate than an existing baseline. We have **one** authentic AI-agent report, no independently blinded evaluation labels and no test-set performance estimate.
- NOT proven academic novelty or publishable methodological contribution.

**Accurate research summary:** "Developed and tested an open-source Python prototype that reproduced two estimands from one publicly released AI-agent statistical analysis using independently written regression code and the original METR dataset; verified eight numerical claims against source-aligned evidence."

## Reproduce

```bash
pip install -e '.[test]'
pip install -r requirements-experiments.txt
curl -L -o metr.csv https://raw.githubusercontent.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv
python -m experiments.independent_metr_reanalysis metr.csv --out results/repro.json
python -m experiments.audit_authentic_metr_claims
pytest -q
```
The audit command currently reads `results/metr_independent_reanalysis_verified.json` saved as a verified result snapshot in the repository (it does not use `results/repro.json` unless modified).
