# AuditCal

**An evidence-aware Python prototype for checking structured statistical claims in AI-generated research reports.**

AuditCal compares reported numerical values with **external, independently obtained evidence**. To avoid false accusations, it returns `UNVERIFIABLE` when provenance is missing, reported and evidence model identifiers disagree, or a valid comparison cannot be established.

> **Scientific status:** Experimental prototype. Not an automatic paper reader, not a semantically model-aware full auditor, and not independently validated for general scientific accuracy or novelty.

## What works

- Checks structured sample counts, coefficients, odds ratios, p-values, confidence intervals, signs and statistical-significance claims.
- Requires human/caller supplied source provenance and **literal model identifiers**; matching strings do not prove statistical specification equivalence.
- Returns `SUPPORTED`, `FLAGGED_DISCREPANCY` or `UNVERIFIABLE`.
- Includes reproducible, case-specific examples derived from authentic released AI-agent reports on pinned METR and Soccer datasets. Original AI-generated programs were **read as untrusted text, not executed**.

## Install and run

Python 3.10+:

```bash
python -m pip install -e '.[test]'
python -m auditcal.cli examples/claims.jsonl
python -m pytest -q
```

Example manually mapped JSONL record:

```json
{"claim_id":"demo-01","claim_type":"sample_size","reported":246,"verified":246,"model_id":"sample-v1","evidence_model_id":"sample-v1","provenance":{"source":"independently_recomputed_pinned_data"}}
```

**Important:** The `verified` field is independently computed *outside* the checker; no source data are fetched by the core function.

## Layout

| Folder | Contents |
|---|---|
| `src/auditcal/` | Auditing core and CLI |
| `tests/` | Software unit/snapshot tests |
| `examples/` | Small input demo |
| `experiments/` | Selected independent data-recomputation scripts |
| `evaluation/` | Frozen pilot protocol, selected claims, source locks and guarded scorer |
| `docs/` | Evidence, limitations and related-work comparison |
| `results/` | Small verified source-data result snapshots |
| `.github/workflows/tests.yml` | Automated checks |

## What the pilot actually showed

Eight original AI-agent reports and eight companion scripts were source-hash verified. Twenty-four numerical claims were frozen under a report-held-out selection procedure. Separate independent calculations showed **10 source-count agreements, 8 straightforward inferential numerical agreements and 6 unresolved methodological/rounding cases** requiring genuine independent statistics review.

In a separate genuine AI-generated Soccer report, two stated distinct-entity counts were inconsistent with the pinned public dataset. These observations **do not** establish a checker accuracy percentage, a population error rate, or causal/scientific validity.

- [Preliminary pilot readout](evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md)
- [Frozen pilot protocol](evaluation/HELDOUT_V01_PROTOCOL.md)
- [Source-backed Soccer count discrepancy](docs/STAGE10_SECOND_DATASET_REAL_AI_COUNT_DISCREPANCIES.md)
- [Existing-method comparison and novelty caveat](docs/STAGE12B_LITERATURE_COMPARISON_MATRIX.md)

## Research question

Can safe, source-data numerical recomputation under a fixed dataset/sample/model/estimand specification—plus principled abstention when these cannot be matched—reduce false numerical warnings compared with a values-only baseline? **This remains a hypothesis**, not a demonstrated novelty or benchmark improvement.

## Boundaries and reproducibility

- No arbitrary uploaded/agent-written code is executed.
- Exact dataset file hashes, model definitions and source references are described in the evaluation documents.
- Genuine blind human gold labels **have not been obtained**; the held-out scorer correctly refuses to output accuracy.
- Multiple adjacent methods already address related code/prose and workflow auditing tasks.
- The repository is a **curated research snapshot**, with the full exploratory investigation preserved in a separate private research repository. Do not claim publicly inspectable branch contents imply a complete standalone provenance archive.

## Reproducibility and sharing

- [Reproducibility guide](docs/REPRODUCIBILITY.md): install dependencies, run the sample CLI and source-backed demonstration, check pinned data hashes.
- [Third-party sources and notices](docs/THIRD_PARTY_SOURCES.md): original data and released-agent source attribution, confirmed license metadata and unresolved reuse conditions.
- [Current research boundaries](docs/RESEARCH_BOUNDARIES.md): separates preliminary source checks from independent scientific validation.
- [Automated software tests](https://github.com/ds-aziz/AuditCal/actions/workflows/tests.yml) verify engineering behavior and the scorer's blocked-without-gold gate. **Passing tests are not claim-auditing accuracy.**
- **License:** no reuse license has been selected. Source inspection is possible where repository access is granted, but reusing it is not automatically permitted. Source data and released AI reports belong to their respective publishers; no external datasets are redistributed here.

This repository contains no applicant CV, scholarship records or outreach lists. Archived research run links in older JSON evidence records refer to an earlier private study and may not be externally accessible; use the included evidence snapshots and sources instead.
