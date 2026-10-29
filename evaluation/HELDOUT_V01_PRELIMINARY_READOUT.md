# Held-out v0.1 — Preliminary Source Integrity and Count Readout

**Provenance note:** Historical CI run IDs below refer to a previous **private** research archive; external readers cannot open those archived job logs. The selected source-data snapshots, scripts, frozen protocol and independent-review status in *this* repository are what can be inspected directly. Previously reported run success is historical and is not a fresh rerun of every experiment.


**As of 2026-10-29 (Asia/Karachi). Evaluation in progress, not a validated accuracy benchmark.**

## Pre-frozen evaluation inputs

- Source-selection manifest: [heldout_v01_manifest.json](heldout_v01_manifest.json).
- Prespecified criteria: [HELDOUT_V01_PROTOCOL.md](HELDOUT_V01_PROTOCOL.md).
- Source-LFS hash lock: [heldout_v01_lfs_sha_lock.json](heldout_v01_lfs_sha_lock.json).
- Before independently recalculating any selected claim: [heldout_v01_selected_claims.json](heldout_v01_selected_claims.json) locked the first three eligible, nonduplicate numerical assertions in each of eight reports, exactly 24 claims.

Two datasets (METR, Soccer), two agent variants (Claude Sonnet 4.5, Qwen3 235B), two runs each, standard persona. This holds out **report directories**, not entirely unseen datasets. Existing Stage 7–11 results were not included as new selected test claims.

## Authentic original source verification

Original upstream commit: d489f03b143fcaa9befb8cc443594ff63ec61eaa. Eight original report files and eight AI-authored analysis scripts (16 source files) all matched the published Git LFS SHA256 object digests, downloaded by GitHub Actions.

- Successful source verification run (historical private CI run 40854026108; access restricted).
- Successful full first-sentences inspection run (historical private CI run 40854338435; access restricted).
- **AI-generated source code was read as static text, NEVER executed.**

## Direct-source counts: 6/6 numerical agreements

Independently verified official METR dataset SHA256: 1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746.
Independently verified university teaching copy of Soccer SHA256: 6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a.

Successful independent raw-source checks (historical private CI run 40854734317; access restricted).

| Frozen claim | Agent reported | Independent calculation |
|---|---:|---:|
| S1-C1, developers | 16 | 16 |
| S1-C2, METR tasks | 246 | 246 |
| S2-C1, METR tasks | 246 | 246 |
| S2-C2, developers | 16 | 16 |
| S4-C1, Soccer source dyads | 146,028 | 146,028 |
| S4-C2, Soccer league countries | 4 | 4 |

Soccer source league values: England, France, Germany, Spain. These six statements contain repeated underlying facts, not six independent study discoveries.

## Independently reconstructed filtered source counts: 4/4 numerical agreements

S3/S7/S8 untrusted model scripts safely inspected as static text (historical private CI run 40854889367; access restricted).
Successful independent reimplementation of the sample filters (historical private CI run 40855127317; access restricted).

| Frozen claim | Agent reported | Independent calculation |
|---|---:|---:|
| S3-C1, complete-case Soccer dyads | 115,457 | 115,457 |
| S7-C1, filtered Soccer dyads | 106,920 | 106,920 |
| S7-C2, league countries under S7 filter | 4 | 4 |
| S8-C1, filtered Soccer dyads | 99,645 | 99,645 |

**Why filters matter:** S3 requires both skin ratings and a parseable birthday plus its complete-case covariates. S7 and S8 compute row-wise mean with a one-rating fallback allowed in principle, then limit skin-tone groups and apply different missing-data filters. On the actual retained S7 and S8 samples, **zero** rows were retained with only one skin rating, so the possible fallback did not actually change these sample counts.

**Only numerical/sample-fidelity checks were performed.** No causal discrimination conclusion follows.

## Integrity of interpretation — what these results DO and DO NOT say

- **16/16 pinned source files SHA-verified**; eight reports available, no source substitution.
- **24 first-eligible statistical claims selected** under fixed original report order. Confidence intervals and p-values count separately; transformed duplicates of the same point estimate do not.
- **10/10 preselected count assertions independently reproduced** (six unfiltered, four method-specific sample/category counts).
- **All 14 inferential/model claims now have independent numerical reference calculations; 8 show straightforward display-precision agreement and 6 require method/rounding/estimand adjudication. See addendum below.**
- **Independent blinded second human gold reviewers: zero.** These numerical results are single-researcher checks, not human-adjudicated gold labels.
- **AuditCal-vs-naive comparator benchmark: NOT RUN.** No precision, recall, false alarm rate or valid overall scientific accuracy estimate exists. Never call 10/10 an AuditCal accuracy metric.
- Soccer source is a pinned educational repository copy. Exact original OSF file-byte identity is **not verified**.
- The current AuditCal core receives manually prepared claim fields and externally calculated evidence; model IDs are caller-provided, not automatically inferred.

**Next scientific steps:** independent review of the six ambiguous claims, then apply the prespecified AuditCal and naive baseline. The frozen original claim list must remain immutable.

**Scientific status:** AuditCal remains a preliminary prototype, not a peer-reviewed, independently validated or established novel statistical auditing method.


---

## Addendum: independent reanalysis of ALL 14 frozen inferential claims (2026-10-29)

**Status: independently recomputed, NOT double-reviewed or adjudicated.** Original AI-authored programs were NEVER run. All source scripts were SHA-verified and inspected only as static text. Reproductions use independent Python implementations on pinned public data.

- Successful frozen METR model reanalysis (historical private CI run 40856299523; access restricted) (developer FE / cluster-t, REML mixed models).
- Successful frozen Soccer model reanalysis (historical private CI run 40856323761; access restricted) (S3 clustered LPM, S4 logistic g-computation, S7 identity-binomial GLM, S8 binomial-trials logit and risk contrasts).
- Original additional five AI scripts inspected as STATIC TEXT (historical private CI run 40855713102; access restricted).
- Both independent computation scripts and GitHub Actions workflows are on the project branch; existing source/test actions passed.

### Frozen claim comparison (reported versus independent)

| Claim | Reported | Independent calculation | Result |
|---|---|---|---|
| S1-C3 | GMR 1.133 | 1.1334766034 | Agrees to displayed decimals |
| S2-C3 | +13.35% | +13.34766034% | Agrees |
| S3-C2 | RD +0.1771 percentage points | +0.17714799 pp | Agrees |
| S3-C3 | 95% CI [-0.0191,0.3734] pp | [-0.01905813,0.37335412] pp | Both endpoints agree |
| S4-C3 | RD +0.25 pp | +0.25302182 pp | Agrees |
| S5-C1 | +10.9% | Literal Python-formula analog +10.94974018%; prose-intended model +11.80243334% | **MODEL AMBIGUITY** |
| S5-C2 | CI [0.941,1.308] | Literal [0.94134277,1.30768996]; intended [0.94880987,1.31741717] | **MODEL AMBIGUITY** |
| S5-C3 | p=0.215 | Literal 0.21530430; intended 0.18272961 | **MODEL AMBIGUITY** |
| S6-C1 | +15.7% | +15.70095502% | Agrees |
| S6-C2 | CI [0.990,1.351] | [0.99049736,1.35151405] | **STRICT ROUNDING BOUNDARY REVIEW**: upper endpoint rounds to 1.352 at three decimals; discrepancy beyond frozen floating margin ~0.000014 |
| S6-C3 | p=0.066 | 0.06583731 | Agrees |
| S7-C3 | RD 0.0020 | 0.0020059475 | Agrees (identity-link/binomial domain warning) |
| S8-C2 | RD +0.0811 pp | Discrete contrast +0.08110194 pp; derivative AME +0.07624410 pp | **ESTIMAND AMBIGUITY** |
| S8-C3 | CI [-0.0002,0.202] pp | Derivative delta-method CI [-0.00020193,0.15269013] pp | **INFERENCE METHOD/INTERVAL MISMATCH** |

### S5: hidden extra covariate from written formula

The released S5 model uses R-like random-effects notation (1 | dev_id) in a Python Patsy fixed-effect formula, AND separately specifies groups=dev_id for the random intercept. In Patsy, that expression evaluates a **bitwise-OR fixed covariate**, not R mixed-model syntax. Independently reproducing the literal effective Python formula (without running the agent program) yielded a GMR of **1.1094974**, CI **[0.9413428,1.3076900]**, p **0.2153043**, matching published values. The prose-intended random-intercept model without the unintended extra predictor yielded GMR **1.1180243**, CI **[0.9488099,1.3174172]**, p **0.1827296**.

This is potentially a **real source-code/report model-description inconsistency**. It must NOT be called a proven statistical reporting error, a fabricated result, or a causal finding without independent expert adjudication. Numerical reproduction of the unexpected bitwise model does not validate the intended research question.

### S8: derivative versus discrete contrast

S8 report risk difference +0.0811 pp matches an independently calculated **discrete binary 0-to-1 standardized probability contrast**, but the script requests derivative marginal effects using get_margeff(method='dydx', at='overall'), and independent delta-method derivative AME is +0.07624410 pp. Its reported CI upper endpoint 0.202 pp does NOT match the derivative CI upper endpoint 0.15269013 pp. Exact estimand and inference sources require review. Do not flag by comparing different legitimate estimands.

### Conservative frozen sample status

- **8 source reports, 16 original LFS files authenticated; 24 claims fixed before analysis.**
- **10 source/count claims matched; 8 additional model-specific claims numerically matched at report precision; 6 require adjudication** (S5-C1, S5-C2, S5-C3, S6-C2, S8-C2, S8-C3).
- **0 independent second human gold labels.** No confirmed statistical inferential errors. No AuditCal-vs-naive baseline evaluation done. No valid precision/recall/accuracy percentage can be calculated or claimed from these numbers.
- Soccer data are still a pinned educational copy, not verified byte-identical to original OSF research deposit.
- This held-out set is by REPORT, not by unfamiliar dataset.

**Next:** Targeted independent statistical-methods review of the six unresolved claims, preserve disagreements, then run the fixed AuditCal and naive baseline without adjusting tolerances after looking at outcomes. Scholarship goal and professor outreach HOLD unchanged.


---

## Focused S8 estimand/CI diagnostic (2026-10-29; no new sample selection)

**Reason:** S8-C2 / S8-C3 are among the six pre-existing unadjudicated claims. This was a *targeted methodological follow-up*, not a new Stage, not a rerun of all 24 claims and not a held-out performance study. Original report and AI-authored code were inspected as hash-locked **static text only** and were **not executed**.

**Code/evidence:** [Independent S8-only diagnostic](../experiments/heldout_v01_s8_method_diagnostic.py), successfully executed GitHub Actions evidence (historical private CI run 40864956460; access restricted), with source educational CSV SHA-256 \`6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a\`, N = 99,645, statsmodels 0.15.0, binomial-trials logit and covariance clustered by \`playerShort\`. The independent model converged without recorded fit warnings. Native statsmodels \`get_margeff\` checks agree with separately implemented analytic gradient/delta-method calculations to numerical precision.

| S8 statistic (units **percentage points** unless noted) | Published report | Matched binary 0→1 **discrete** contrast | Matched **derivative** marginal effect |
|---|---:|---:|---:|
| Effect | +0.0811 pp | +0.08110194 pp | +0.07624410 pp |
| Two-sided p-value | 0.051 | 0.06549447 | 0.05060824 |
| 95% normal/delta CI | [-0.0002, **0.202**] pp | [-0.00520006, 0.16740394] pp | [-0.00020193, 0.15269013] pp |

**Specific provenance issue:** In the released S8 source script, \`result.get_margeff(method='dydx', at='overall')\` was called with **no \`dummy=True\` argument** (source lines 54–62); that default computes a *derivative* marginal effect. The report's **point estimate** reproduces the **discrete binary contrast**, while the report's **p=0.051** and 95% CI **lower endpoint -0.0002 pp** reproduce the **derivative** inference at printed precision. The reported **upper endpoint 0.202 pp** matches neither checked standard method. Moreover, the report's interval midpoint is **0.1009 pp**, not its reported effect **0.0811 pp**, whereas the source code's normal/Wald \`margeff.conf_int\` is symmetric around its estimate. This suggests possible mixing/misreporting of inferential quantities in the original prose, **not** a proven gold-label error. There may be additional unobserved analysis steps; independent expert review is necessary before assigning an error type.

**Frozen-evaluation integrity:** S8-C2 (point) and S8-C3 (CI) were part of the original 24 first-three-claim sample. The published p=0.051 is shown here for **context only**; it was **not** selected in the original first-three sample and MUST NOT be added to the scorecard denominator after observing it.

**Status unchanged:** Both S8-C2 and S8-C3 remain unadjudicated; total held-out v0.1 remains **10 source-count matches + 8 preliminary inferential agreements + 6 requiring qualified human review**, no 24-case gold labels and no measured AuditCal accuracy. This result clarifies **why** external methodological review matters; it does not replace it.


---

## Focused S5 formula semantics + S6 precision boundary (2026-10-29)

**Scope and independence:** This is a narrow mechanistic follow-up on already frozen unresolved cases **S5-C1/C2/C3 and S6-C2**. It does **not** change source report selection, add claims, re-run prior model fits, or constitute independent human adjudication. The independent 2026-10-29 source-data numerical model fit from METR inference run 40856299523 (historical private CI run 40856299523; access restricted) supplies the *existing* full-precision numerical reference values.

**New tested diagnostic:** [Independent S5/S6 formula-and-rounding script](../experiments/heldout_v01_s5_s6_method_diagnostic.py), successful GitHub run 40865720769 (historical private CI run 40865720769; access restricted). Official METR source SHA256 is still \`1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746\`; **246 rows, 16 developer IDs**. The original AI-authored source was read as static text, never executed. This new diagnostic **only builds Patsy design matrices** and checks decimal boundaries; no regression model was re-fitted in the diagnostic.

### S5: concrete Python source-formula proof

The released S5 analysis code has the formula string \`np.log(initial_implementation_time) ~ ai_treatment + predicted_time_no_ai + (1 | dev_id)\` (original source lines 16–19), and independently passes \`groups=df["dev_id"]\` to \`smf.mixedlm\`. An actual *Patsy 1.0.3* factor-construction check on the hash-pinned METR CSV produced:

- **Intended fixed-design columns:** \`Intercept\`, \`ai_treatment\`, \`predicted_time_no_ai\`.
- **Literal original-formula fixed-design columns:** exactly those **plus** a fourth fixed covariate named \`1 | dev_id\`.
- Every element in that extra covariate is **exactly** \`np.bitwise_or(1, dev_id)\` using the integer source developer IDs. This is not R random-intercept syntax; the separate \`groups=\` argument provides the genuine random intercept.

This confirms the **executable meaning of the formula text**, rather than inferring it from numeric similarity. It does **not** show whether a real user would have intended the extra predictor; the report describes the usual random-intercept model without mentioning it.

**Both rounded quantities near a boundary:** independently re-fitted *literal design analogue* yielded **+10.9497401823%**, which is within the 1-decimal reported **+10.9%** interval (distance to 10.95% halfpoint 0.0002598177 pp); and ratio **1.1094974018**, which rounds to reported **1.109** at three decimals (distance to 1.1095 halfpoint 0.0000025982). Literal CI **[0.94134277,1.30768996]** and p **0.21530430** also meet original display precision; the prose-intended no-extra-covariate model instead yields **+11.80243334%**, ratio **1.11802433**, CI **[0.94880987,1.31741717]**, p **0.18272961**. These numbers were calculated *previously*, not re-fitted in this narrow source diagnostic.

**Interim classification:** **source-code/prose model-description inconsistency candidate**, numerically reported estimates replicate the *literal* effective model. **S5-C1/C2/C3 remain unadjudicated pending a genuine blind independent statistician**; not a proven false causal finding or guaranteed model-invalidity verdict.

### S6: unmodified frozen decimal interval rule

The original released S6 code (source lines 24–32, 59–66) uses \`result_primary.conf_int()\`, exponentiates it, then prints endpoints with three decimals. Previous source-data refitting gave independent CI \`[0.9904973579860092,1.351514053588001]\` versus reported \`[0.990,1.351]\`.

| S6 endpoint | Published | Independent | Absolute difference | Maximum at 3 decimals + original 1e-8 margin | Frozen numeric rule |
|---|---:|---:|---:|---:|---|
| Lower | 0.990 | 0.9904973579860092 | 0.000497357986 | 0.00050001 | **Pass** |
| Upper | 1.351 | 1.351514053588001 | 0.000514053588 | 0.00050001 | **Outside** by 0.000014043588 above allowed margin |

The upper independently calculated value rounds **1.352**, whereas the AI report prints **1.351**. Using the original unrelaxed half-display-unit rule, this specific numerical discrepancy **does not pass**. Its distance outside the raw half-unit boundary is \`0.000014053588001\`; beyond the extra permitted 1e-8 margin it is \`0.000014043588001\`. A library/optimizer-version difference or another inference detail might explain this tiny difference, **but that remains a hypothesis**, not an excuse to silently change rounding rules.

**Interim classification:** **borderline upper CI endpoint mismatch requiring statistical-method/version review**, not a proved consequential scientific error. **S6-C2 remains unadjudicated**.

### Research integrity and next dependency

- The six original pending cases remain **S5-C1/C2/C3, S6-C2, S8-C2/C3**. S8's separately verified discrete/derivative analysis is in the preceding addendum.
- No independent human expert has approved gold labels. No AuditCal-vs-naive held-out performance score has been generated. The previously viewed 24 examples are retrospective for newer scoring code; do not claim unseen accuracy.
- Reviewer-facing [blind instructions](HELDOUT_V01_BLIND_REVIEW_GUIDE.md) are left unchanged **to preserve the reviewer not seeing our findings** before their own assessment.
