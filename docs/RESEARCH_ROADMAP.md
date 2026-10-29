# Proposed Master's research roadmap

**Status: Future research proposal, NOT completed research or a supervisor-approved thesis.**

## Research direction
Trustworthy AI for Scientific Research and Reproducible Statistical Analysis.

**Question:** Under genuinely matched dataset/sample/model/estimand conditions, can independent numerical recomputation with principled abstention reduce false warnings about legitimate but different scientific analyses, compared with a values-only checker?

## Preparatory work already completed
- A manually structured Python checker, CLI, test suite, safe refusal/abstention logic, numerical source snapshots and independently written case-specific research scripts.
- Published source-hash-checked AI-agent reports and original source data studies across METR and Soccer; two actual Soccer report count inconsistencies in one report.
- Eight-report, 24-selected-claim exploratory pilot: 10 count agreements, eight straightforward inferential numeric agreements, six method/inference ambiguous cases; **no independently human-reviewed gold labels**.
- Targeted case studies: S5 Python Patsy formula semantics, S6 marginal CI rounding difference, S8 discrete-versus-derivative marginal effect confusion.
- Related-work comparison against statcheck, PaperAudit, ForkSCOPE and AI analyst/process auditing. Novelty and better-than-baseline performance have **not** been demonstrated.

## Proposed research work (not yet achieved)
1. **Define a precise claim–evidence specification:** record dataset hash/version, filters, population, outcome, transformation, model family, estimand, variance estimator, rounding and missing-evidence conditions.
2. **Develop a safe bounded verifier:** independently recompute selected count/inferential claim families and explain non-comparability. Avoid running arbitrary AI-generated code.
3. **Build a credible prospective evaluation set:** obtain qualified blind reviewers, adjudicate disagreements, and lock criteria before accessing *new* task/report test outcomes.
4. **Measure against appropriate baselines:** values-only matching, simple rule checks, and eligible prior tools. Separate changes in information access from improvements in verification logic.
5. **Analyze failure modes, abstention and cost:** false-warning rate on defensible analyses, recall on genuine unsupported claims, precision when defined, abstention coverage, robustness across datasets/agent models, statistical uncertainty and reviewer/computational cost.
6. **Produce a reproducible thesis:** source manifests, permitted code/data documentation, limitations, and negative or inconclusive results.

## Possible degree phases
| Phase | Study and research activity | Evidence-based deliverable |
|---|---|---|
| Foundation | Advanced statistics/ML, literature review, supervisor-guided scope selection | Revised research question and related-work review |
| Method design | Explicit model/estimand matching, provenance rules, safe computations | Bounded checker and defined comparison protocol |
| Independent assessment | Blind statistical reviewers, gold-label design, untouched tasks | Adjudication, locked test corpus and uncertainty plan |
| Empirical evaluation | Paired baselines and method ablations | Replicable error/false-warning/coverage results |
| Thesis | Interpretation, scientific write-up, reproducibility and defense | Dissertation and released permitted research artifacts |

**Timing is illustrative:** actual Master's degrees may be 2, 2.5 or 3 years; requirements, facilities and supervision determine the approved schedule.

## Integrity and feasibility gates
- Six difficult cases remain unadjudicated without genuine external statistical review.
- The earlier 24 examples have already informed research software choices; they cannot subsequently be claimed as untouched prospective evaluation cases.
- Source datasets and upstream study artifacts may have independent licenses; only share what is permitted.
- Verification of numerical values is not a substitute for causal identification, sampling-design validity, ethical review or domain-scientific expertise.
- Adjacent published work already performs code/prose auditing and agent-workflow checking; a narrower defensible contribution needs a measured comparison.
- A negative result or a bounded abstention tool can be a useful outcome when reported transparently.

See [completed evidence](../evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md), [protocol](../evaluation/HELDOUT_V01_PROTOCOL.md), and [method comparison](STAGE12B_LITERATURE_COMPARISON_MATRIX.md).
