# AuditCal

**Evidence-grounded checking of numerical claims in AI-assisted scientific analysis**

AuditCal is a Python research prototype that compares **manually structured numerical claims** with **independently recomputed, source-backed evidence**. When the dataset, sample, statistical specification, or evidence cannot be matched, a verifier should **abstain rather than confidently call a result wrong**.

## Research problem

An AI-generated research report can contain a numerical inconsistency. But two legitimate analyses of the same question can also differ because their filters, models, estimands, or uncertainty methods differ. AuditCal studies how reproducible numerical checks can respect this distinction.

**Research question:** Can bounded independent recomputation, with explicit abstention when statistical comparisons are unjustified, reduce false numerical warnings compared with values-only checking?

This is a **research hypothesis**, not a demonstrated new algorithm or validated accuracy improvement.

## What has been implemented

- **Python checker:** `src/auditcal/` checks manually mapped sample sizes, counts, estimates, confidence intervals, p-values and related claims against **externally supplied** numerical evidence.
- **Outcomes:** `SUPPORTED`, `FLAGGED_DISCREPANCY` or `UNVERIFIABLE`. Caller-defined matching model IDs are not automatic statistical-method understanding.
- **Command line + example:** `src/auditcal/cli.py` and `examples/claims.jsonl`.
- **Independent research scripts:** `experiments/` contains source-data reanalyses, verification of original reports and alternative model/marginal-effect checks. Original AI-authored scripts were inspected as **untrusted text**, not executed.
- **Evidence and safeguards:** hashed-source manifests, selected result snapshots, original pilot protocol, blank independent-review templates, values-only baseline and a scoring gate that refuses to report accuracy until genuine independent gold labels and predictions exist.
- **Research reproducibility:** tests, methodology, historical research notes and preserved **inactive** experiment-workflow recipes.

## What our authentic-data investigations found

| Research step | Completed work | Evidence |
|---|---|---|
| Source acquisition | Acquired and checked authenticity of published AI-agent research reports and companion scripts | [Provenance](docs/PUBLISHED_AGENT_REPORT_SOURCE.md) |
| METR | Independently reproduced selected model outputs from an authentic AI report, compared specifications and examined original code as text | [METR research](docs/STAGE7_AUTHENTIC_AGENT_INDEPENDENT_REANALYSIS.md) |
| Multi-agent research | Inspected 10 original reports from five prompt conditions and compared selected numerical results across other model families | [Stage 8](docs/STAGE8_TEN_GENUINE_REPORTS_AND_METHOD_VARIANTS.md) · [Stage 9](docs/STAGE9_CROSS_MODEL_REPRODUCIBILITY_REPORT.md) |
| Soccer data audit | Source-derived filtered sample: **99,535 dyads**, **1,214 players** and **2,758 referees**; the original AI report gave **99,535**, **9,959** and **2,103** respectively | [Two verified source-count disagreements](docs/STAGE10_SECOND_DATASET_REAL_AI_COUNT_DISCREPANCIES.md) |
| Method interpretation | Diagnosed Python formula semantics (S5), a borderline reported interval endpoint (S6) and an estimand/interval-method conflict (S8) | [Current pilot readout](evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md) |
| Frozen pilot | **8 authentic reports, 24 frozen numerical claims**. Independent calculations found **10 count agreements**, **8 straightforward inferential agreements** and **6 unclear inferential cases** requiring independent statistical adjudication | [Protocol](evaluation/HELDOUT_V01_PROTOCOL.md) · [Readout](evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md) |

The **18 initial agreements are not 18/24 AuditCal accuracy**. The held-out unit was the **report**, not a new dataset. Qualified independent blind reviewers have **not** supplied final gold labels. Baseline/scorer implementations came after these exploratory observations, so the same 24 examples are **not a fresh prospective performance test**. Source-matched numerical agreement does not validate causal interpretation.

[Chronological research history](docs/RESEARCH_HISTORY_INDEX.md) includes the earlier investigations and source-linked record.

## Proposed Master's research — not completed yet

**Research direction:** Trustworthy AI for Scientific Research, Reproducible Data Science, Statistical Machine Learning.

A future supervised research programme could:

1. Record a clear **source–sample–model–estimand–uncertainty contract** for each claim to determine whether a comparison is actually justified.
2. Extend **safe, bounded numerical verification** to carefully selected statistical tasks, with transparent provenance and abstention.
3. Obtain **independent qualified statistical judgments**, freeze an evaluation protocol and assemble genuinely *new* held-out tasks/reports.
4. Compare values-only matching, rule-based verification and applicable existing auditors on the *same* evidence; measure false warnings, recall, coverage, abstention, cost and uncertainty.
5. Report negative results and limitations, and produce a reproducible thesis contribution if the evidence supports one.

This is a proposed research programme, **not proof of novelty, professor acceptance, or thesis results**. [Detailed Master's research roadmap](docs/RESEARCH_ROADMAP.md).

## Run the software

Python 3.10+:

```bash
python -m pip install -e '.[test]'
python -m pip install -r requirements-experiments.txt
python -m pytest -q
python -m auditcal.cli examples/claims.jsonl
```

Example manually structured input (the verified value was calculated **outside** AuditCal):

```json
{"claim_id":"demo-01","claim_type":"sample_size","reported":246,"verified":246,"model_id":"sample-v1","evidence_model_id":"sample-v1","provenance":{"source":"independent_source_count"}}
```

[Reproducibility guide](docs/REPRODUCIBILITY.md) explains which commands use bundled numerical snapshots and which require a separately downloaded, SHA-256-verified source dataset.

## Repository map

| Location | Purpose |
|---|---|
| `src/auditcal/` | Python checker and CLI |
| `examples/` | Example input |
| `tests/` | Software/unit/source-snapshot and import tests |
| `experiments/` | Independent reproducibility and real-report research scripts |
| `results/` | Original selected numerical evidence snapshots |
| `evaluation/` | Frozen protocol, original case selection, baseline, review templates and guarded scorer |
| `docs/` | Methodology, scientific readouts, limitations, research history and future roadmap |
| `reproducibility/historical_workflows/` | Preserved **inactive** older research-run recipes |
| `.github/workflows/tests.yml` | Current active automated software tests |

[Current limitations](docs/RESEARCH_BOUNDARIES.md) · [Related work](docs/STAGE12B_LITERATURE_COMPARISON_MATRIX.md) · [Sources/attribution](docs/THIRD_PARTY_SOURCES.md)

**Software tests assess engineering behavior, not the system's real-world statistical accuracy.**
