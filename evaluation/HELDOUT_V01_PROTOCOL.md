# AuditCal — Small Held-Out Report Pilot, v0.1 Evaluation Protocol
**Project:** AuditCal / Trustworthy AI for Scientific Research
**Protocol freeze date:** 2026-10-29 (Asia/Karachi)
**Status at protocol freezing:** This protocol and report-selection manifest were frozen before case recomputation. **Updated research status:** 24 original claims have now received exploratory source-data investigation (18 preliminary numerical agreements, 6 unresolved); independent human gold labels and scientifically valid AuditCal accuracy metrics are still absent. Read the [preliminary readout](HELDOUT_V01_PRELIMINARY_READOUT.md) for the subsequently recorded results. Original case-selection and comparison rules below are preserved.
**Frozen selection manifest:** [heldout_v01_manifest.json](heldout_v01_manifest.json)
**Prior work:** Stage 7–11 METR/Soccer exploratory audits were used for method design. Their previously inspected claims are **not** evaluation examples here.
**Research identity:** Check whether same-source and same-method numerical errors can be identified *without falsely declaring valid alternative statistical specifications erroneous*. Avoid broad claim of general AI reliability.

## 1. Questions and scope

**RQ1 (numerical fidelity):** For a fixed previously uninspected report subset, can AuditCal identify source-backed numerical reporting discrepancies, rather than merely reproduce manually selected examples?

**RQ2 (method differences):** When the same underlying data permits multiple defensible models/estimands, does specification-aware abstention avoid flags that a naive values-only comparator would generate?

**RQ3 (coverage):** How often can the system give a warranted decision versus abstaining because data, method or evidence is insufficiently specified?

This is a **small exploratory held-out-report pilot within two already familiar datasets**, *not* a held-out-dataset generalization benchmark; no hypothesis of model superiority or accuracy threshold will be claimed on these small counts.

## 2. Preselected sample (locked before reading these reports)

The public upstream repository `amazon-science/agentic-forking-path` is pinned at Git commit `d489f03b143fcaa9befb8cc443594ff63ec61eaa`. Its GitHub directory **metadata** was inspected to verify candidate folders and `mirrored_report.txt` / `final_analysis.py` entries, without inspecting these eight candidates' report/code contents or numerical outcomes during this selection.

Eight directories were frozen in [the machine-readable manifest](heldout_v01_manifest.json): **standard persona, 2 datasets (METR/Soccer) × 2 model variants (Claude Sonnet 4.5/Qwen3 235B) × 2 runs**. These are the **third and fourth timestamp-sorted folders** in each of these four cells. Earlier first/second runs were the primary material in previous METR/Claude Soccer studies; Qwen Soccer first was previously studied. Third/fourth are chosen mechanically, not based on whether reports appear correct.

Report IDs (actual path/source identifiers are in the manifest):

| ID | Dataset | Model | Run timestamp directory |
|---|---|---|---|
| S1 | METR | Claude Sonnet 4.5 | 2025-11-12T19-03-00+0000 |
| S2 | METR | Claude Sonnet 4.5 | 2025-11-12T19-45-03+0000 |
| S3 | Soccer | Claude Sonnet 4.5 | 2025-11-12T18-01-53+0000 |
| S4 | Soccer | Claude Sonnet 4.5 | 2025-11-12T18-56-42+0000 |
| S5 | METR | Qwen3 235B | 2025-12-11T22-29-20+0000 |
| S6 | METR | Qwen3 235B | 2025-12-11T22-35-55+0000 |
| S7 | Soccer | Qwen3 235B | 2025-12-11T19-39-27+0000 |
| S8 | Soccer | Qwen3 235B | 2025-12-11T22-21-05+0000 |

**Required verification on first read:** compare actual downloaded report/code SHA-256 bytes to pinned upstream Git LFS object identifiers; log mismatches, failures and exclusions. Never execute upstream untrusted agent-authored scripts; inspect as text only. For Soccer, use the already pinned *teaching copy* of dataset with documented unresolved OSF byte equivalence; for METR use already hash-locked official CSV. Downloading a matched public report doesn't automatically establish that its statistical calculations were correct.

**No substitution:** If a report is unreadable, hash mismatched, contains no eligible claims, or its calculations are difficult, record it as missing/not adjudicable/zero eligible according to the rule below. **Do not replace it with a conveniently better report.** Previously audited report/source overlap discovered after freeze must be logged with source IDs and removed from held-out metrics without replacement. Keep a separate audit trail.

## 3. Claim sampling, before numerical outcome inspection

**Target = at most 3 distinct eligible claims/report, hence maximum 24 naturally occurring report claims.** Read each report *in original file order*, including Executive Summary / Findings / Results. Record the **first three nonduplicate explicit numerical statistical assertions**, limited to these predefined categories: sample-size, distinct-entity count, coefficient/odds ratio/effect estimate, confidence interval (one claim per interval), and statistical p-value. A p-value accompanied by its own confidence interval is **two claims** if separately asserted. Exclude publication dates, author identifiers, citation numbers, software versions, category labels and purely hypothetical calculations. A repeated figure describing the same statistic/model/sample counts once (keep earliest). For a reported comparison containing several distinct numbers, take them in textual order. No after-the-fact replacement of hard-to-check claims.

**Extraction log:** keep source report SHA, exact excerpt (brief for audit/internal review), line/offset, measurement units, reported precision, purported population/sample/inclusion filter, transformation, formula or regression, grouping/standard-error method, estimand, model ID and reason for category/eligibility. Record whether the model and source data are actually identifiable. If a selected claim lacks enough information, **retain it and adjudicate 'insufficient evidence'**; do not silently drop it. If there are fewer than three, evaluate all available and log the denominator. The claim extraction step is a *manual, preregistered annotation procedure* — not evidence the checker extracts text automatically.

**Selection independence:** These eight candidates were not selected by observed performance. The corpus shares underlying data/agents with previous experiments, so there is still familiarity and design leakage risk; report these limitations clearly.

## 4. What exactly counts as correct, wrong or uncheckable?

Construct an independent evidence sheet for each selected claim **before running the checker**:
- `SUPPORTED_GOLD`: independent calculation confirms the reported figure for its explicitly matched source dataset/version, filters, variable definitions, transformation, statistical method, estimand and stated rounding.
- `ERROR_GOLD`: material numeric disagreement persists after *same-specification* independent recomputation or proves impossible from source cardinalities, after checking standard error, model and reported rounding. Explain alternative plausible causes.
- `INSUFFICIENT_GOLD`: source/model/estimand/CI or p inference procedure cannot be aligned, data unavailable, report ambiguous, or independent reproduction fails/inconclusive. This is NOT a proven error and NOT a proven correct report.

A different legitimate model, shifted log transform, bootstrap versus asymptotic CI, derivative marginal effect versus discrete 0-to-1 contrast or different source filters must **not** be automatically labelled `ERROR_GOLD`. A numerical match is not a certificate of causal or scientific validity. For borderline discrepancies seek an independent statistician; the published source script's numbers are **not** ground truth just because the agent wrote the code.

**Rounding rule locked before checking:**
- nonnegative integral counts: exact equality; nonintegral/negative reported counts invalid;
- values reported to `d` decimal places (e.g. `0.0158`, `1.246`): independent values should round to the displayed figure at `d` places; allow at most **1e-8 absolute floating-point margin** at the corresponding rounding-interval boundary;
- confidence intervals: apply endpoint rounding separately; require same CI method, confidence level and grouping;
- inequalities / very small p (e.g. `p < .001`) are predicates, **not exact-number matches**; if unsupported by existing checker, record as insufficient/unsupported rather than invent a precise p-value;
- if report expresses an estimate in percentage points, convert to the same units *before* comparing;
- don't loosen tolerances after discovering an inconvenient discrepancy. Pre-specified presentation rounding does not override uncertainty/specification ambiguities.

This is a **gold-label adjudication rule**, not a claim that the existing AuditCal core automatically enforces display-precision rounding. Adapter code would have to supply a compatible fixed tolerance or upgrade the evaluator transparently and test it before predictions.

## 5. Reviewer independence and evidence control

**Two reviewers, independently**, should label each claim using source data and method details; preferably the second reviewer has statistics expertise and has not inspected AuditCal's predictions. Require source references, exact model code written independently from any agent program, method identification, computation logs and label reasoning. Resolve label disagreements only after logging both originals, via documented joint adjudication or a third reviewer. Keep claims unresolved if no agreement; don't fabricate 'independent review' where none exists.

Prevent avoidable leakage by freezing: (a) source report IDs, (b) first-three claims rule, (c) numerical matching/rounding, (d) evaluation criteria, (e) baseline design **before** running AuditCal on these claims. If solo preliminary analyses are performed earlier, label the results `SINGLE-REVIEWER_EXPLORATORY`, not independent gold-standard reliability.

## 6. AuditCal and realistic baselines

**AuditCal target:** existing conservative core accepts *manually structured* reported claims and *externally supplied* numeric evidence; model identity is currently a **caller-provided string equality safeguard**, not automatic semantic model matching. Stage 11 independent regression code is case-specific, not universal automatic source refitting.

**Baseline A (mandatory, feasible):** a naive numeric value comparator that uses the exact same independently produced source evidence but *ignores model/specification identity*; match type and frozen rounding, and flag differing numbers. On model-mismatched pairs the expected danger is a false flag; missing evidence stays missing, not invented.

**Baseline B (optional, clearly disclosed):** LLM-only reviewer given report excerpt and the same *allowed source artifact context*. Use a fixed model/version/prompt and one frozen inference configuration, record costs; avoid letting it see gold labels. If not available, report 'not run' rather than claim comparison.

**statcheck (conditional):** only on genuinely applicable APA-format significance test results with relevant test statistics and df. It is not a valid baseline for distinct-player counts, regression ORs without requisite reported statistics, or unidentifiable sampling.

**Method-mismatch challenge set:** Construct pairs based on **real previously documented alternative legitimate model/estimand results** (e.g. Stage 8 method variations), independent of the eight report evaluation claims, with full documentation of why those models differ. Label these `DO_NOT_FLAG_AS_SAME_MODEL_ERROR`; correct behavior is to abstain rather than claim support. Treat as **separate robustness challenge**, not evidence of naturally occurring authentic error rates. Freeze pair count/identity before running checker.

**Synthetic controlled errors (optional):** create in a **separate** explicitly tagged test pool *only after independent source verification* by a deterministic written corruption rule; don't mix them with authentic reporting error rates. If no controlled errors, recall may be undefined and must be reported as such.

## 7. Metrics, denominators, uncertainty

Maintain a 3×3 count table (`SUPPORTED_GOLD`, `ERROR_GOLD`, `INSUFFICIENT_GOLD` × `SUPPORTED`, `FLAGGED_DISCREPANCY`, `UNVERIFIABLE`). Report **all 8 reports**, number of attempted claims, accessible reports, number adjudicated and number not resolved.

Primary descriptive rates:
- **Coverage:** proportion of selected claims receiving a decision (`SUPPORTED` or `FLAGGED`) out of *all selected claims*. Report separately on gold-adjudicable cases.
- **Error-flag precision:** among flags on gold-adjudicable examples, fraction truly `ERROR_GOLD`; do **not** silently remove improper flags on insufficient-gold cases—list them separately as unsafe calls.
- **Recall (errors):** among `ERROR_GOLD` examples, fraction correctly flagged (abstentions count as missed detection for this metric, report separately).
- **False-flag rate:** among `SUPPORTED_GOLD` examples, fraction flagged incorrectly; report **per report/model/dataset** where denominators allow.
- **Improper decisive calls:** supported/flagged responses on `INSUFFICIENT_GOLD`, plus justified-abstention rate on those claims.
- **Method-challenge false flags:** on alternative-method pairs, % labelled discrepancy when correct reaction is to abstain.
- **Baseline comparison:** provide paired case-by-case outcomes and denominators; do NOT compare non-overlapping tasks or call a non-comparison 'outperformance'.

Report numerators, denominators, source categories, and Wilson 95% intervals only where meaningful; with ≤24 correlated claims and 8 reports, uncertainty is large and no population-level generalization or formal statistical superiority claim is justified. If zero gold errors occur, error recall is **undefined**, not 100% (same for precision with zero flags).

## 8. Execution sequence, stop rule and protection against shifting goals

1. **FROZEN NOW:** Source manifest and this protocol committed **before any of these candidate reports' contents or new accuracy outcomes are checked for this pilot**. Record their Git commits/links.
2. Verify upstream LFS source hashes and pinned dataset copy; log attrition/overlaps; read reports as untrusted text and select first eligible 3 by frozen rule.
3. Build and archive blind claim/evidence sheets; obtain second independent reviewer. If unavailable, keep status provisional.
4. Run AuditCal and mandatory naive baseline on locked claims; optionally run comparable LLM-only assessment and separate method challenge.
5. Summarize confusion table and conservative descriptive metrics, uncertainty and failures. No report replacement or post hoc tolerance changes.
6. If the checker requires changes *after inspecting these selected report results*, version code and **treat performance as exploratory development data**, then construct a new distinct held-out sample for a fair evaluation; do not claim the updated checker was tested on unseen examples here.

**Stop at eight source-selected reports / no more than three selected claims per report.** No infinite additional experiments to improve a metric; first discuss whether the findings materially strengthen the scientific research question and whether additional research is warranted.

## 9. Status table and next dependency

| Component | Status as of protocol commit |
|---|---|
| Report-selection rule and eight upstream directories | **DONE, manifest frozen, contents not read for this pilot** |
| Exact report/code SHA-256 byte verification | NOT DONE for these eight |
| First-three claims per report extraction | NOT DONE |
| Human independent source-data gold labels | NOT DONE |
| Real AuditCal/naive comparator predictions | NOT DONE |
| Blind double review | NOT DONE |
| Measured reliability, coverage and false-flag rates | **NOT AVAILABLE** |
| Scientific novelty claim / independent benchmark superiority | **NOT ESTABLISHED** |
| CV / statement of purpose / professor fit review | PENDING IN PARALLEL |

**Scholarship-safe interpretation:** A reproducible pilot protocol with preselected source reports is a meaningful methodological planning deliverable, but it is **not proof of performance**. The existing working project remains a legitimate preliminary research portfolio example. Professor emails remain ON HOLD pending agreed readiness review.


---

## Execution-readiness addendum (2026-10-29; original selection/label rules unchanged)

**This section is an implementation-status addendum made AFTER the eight original reports and their preliminary 24 numerical outcomes were inspected.** It does not rewrite the historically frozen sampling protocol, and the code added now **must not** be represented as having been independently prospectively tested on those already observed outcomes.

### Newly implemented, tested software-only infrastructure
- [heldout_v01_scoring_gate.py](heldout_v01_scoring_gate.py) validates **all 24 original claim IDs and source report SHA-256 values**, requires two distinct self-attested blind independent human review sheets with full source/method/reanalysis rationale, rejects unreconciled disagreements, and refuses a scientific score when either reviewers or paired predictions are missing. A file's written attestation is not an independent proof of real human identity or statistical expertise.
- [naive_values_baseline.py](naive_values_baseline.py) implements **values-only** comparison, deliberately ignoring model/sample/estimand identity. It requires known common units, independently supplied numeric evidence and **pre-declared precision from the original printed source**, including distinct endpoint precision for CIs. Counts compare exactly. It abstains if evidence, units or precision are not defensibly supplied. A difference caused by model variation is not a demonstrated real reporting error.
- [blank full 24-claim review sheet](heldout_v01_blank_full_24_review.json) and [blank paired prediction sheet](heldout_v01_blank_paired_predictions.json) contain **nulls, not manufactured labels or verdicts**. The earlier six-claim [targeted reviewer sheet](heldout_v01_blank_external_review.json) is NOT a substitute for a blind review of the full 24 examples.
- New software unit tests exercise artificial input cases only. They show that, **by construction**, the current AuditCal core abstains when model IDs differ whereas a values-only checker might flag differing numbers. These tests **do not measure false-alarm reduction on real research claims**.

Run \`python evaluation/heldout_v01_scoring_gate.py\` without reviews/predictions: it prints a **BLOCKED_PENDING_INDEPENDENT_GOLD_AND_PAIRED_PREDICTIONS** status and **NO accuracy**. When two complete genuine reviewers, exact frozen-source claim identifiers, disagreements, and paired reproducible predictions are independently resolved, the scoring command is:

\`\`\`bash
python evaluation/heldout_v01_scoring_gate.py \
  --review-one PATH_TO_FIRST_REAL_BLIND_REVIEW.json \
  --review-two PATH_TO_SECOND_REAL_BLIND_REVIEW.json \
  --predictions PATH_TO_REPRODUCIBLY_GENERATED_PAIRED_PREDICTIONS.json \
  --output results/heldout_v01/reviewed_paired_scorecard.json
\`\`\`

It reports the 3×3 gold-versus-output matrix, gold-checkable error precision/recall/false-flag rate, full selection coverage, explicit abstentions/unsafe calls and descriptive Wilson 95% intervals with numerator and denominator. Metrics with zero denominators remain **undefined** rather than set to 100%. Correlated claims and 8-report scope prohibit a general accuracy claim.

### What still prevents research conclusions
1. Real independent **human** reviewers have **not** filled the blank forms or passed external identity/competence verification.
2. No complete 24-case prediction/evidence manifest and **no observed AuditCal-versus-naive 24-case result** exist. The scorecard is a calculation *tool*, not the experimental data.
3. Model IDs in AuditCal's current core are still manually supplied strings; automatic semantic equivalence is not established.
4. Because these particular software implementations were built after observing the 24-case preliminary outcomes, even a later paired analysis on the same data should be described transparently as **retrospective/exploratory**. A subsequent *untouched* report/dataset test would be needed to support a fully prospective claim about these implementations. Do not rebrand this pilot as newly held out by dataset or as external performance validation.

**Evaluation integrity:** No independent expert adjudication, valid system-level accuracy or demonstrated baseline superiority is claimed.
