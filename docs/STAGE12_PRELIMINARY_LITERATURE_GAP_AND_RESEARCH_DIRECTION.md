> **Historical research-stage record.** Read the [current research summary](../README.md) and [research roadmap](RESEARCH_ROADMAP.md) for the latest implemented scope and proposed work. Historical stage-specific claims may precede later investigation.

# Stage 12 — Preliminary Literature-Gap Assessment and Master's Research Direction

**Project:** AuditCal | **Date:** 2026-10-29 (Pakistan time) | **Status:** Preliminary literature mapping, **NOT** a completed systematic review or demonstrated novelty.

## Why this stage exists

The research direction is trustworthy AI, reproducible data science, and source-backed verification of AI-generated scientific analyses, without manufactured accuracy claims.

**Proposed research interest:** Trustworthy AI for scientific research.

**Problem statement:** AI agents can generate plausible statistical research reports, but numerical fidelity, appropriate statistical specification, and interpretation are not interchangeable.

**Proposed master's research question (subject to literature review and supervisor fit):** How can a method-aware verification system detect genuine numerical/statistical reporting errors in AI-generated research while reducing false accusations caused by defensible differences in model specifications and inference procedures?

## Relevant existing work (direct sources checked)

1. **Nuijten et al. (2016), statcheck, Behavior Research Methods.** A well-established automatic statistical reporting inconsistency checker for NHST results from published texts. It recomputes p-values from reported statistics/df and accounts for rounding; it is not a general original-data refitting engine. Thus *automatic statistical fact checking itself is NOT novel*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5101263/

2. **Javaji et al. (2025), CLAIM-BENCH, IJCNLP-AACL.** Evaluates LLM extraction and validation of scientific claims against textual evidence using >300 claim-evidence pairs. Strong overlap with automated claim–evidence verification; our proposed emphasis is original-source data and specified-model numerical reanalysis, which must be empirically compared. https://aclanthology.org/2025.ijcnlp-long.127/

3. **Miao, Pritchard & Zou (2026), The Agentic Garden of Forking Paths, arXiv.** Shows AI scientific agents can reach divergent conclusions through statistically defensible choices; introduces multiverse-oriented analysis and Agentic Bootstrap. Critically relevant: *different p-values are not necessarily calculation errors*. AuditCal's METR/Soccer experiments sourced authentic reports from the accompanying open repository, so this paper is also our source provenance. Not an independent claim of originality. https://arxiv.org/abs/2607.01507

4. **Tu et al. (2026), PaperAudit-Bench, EMNLP.** A full-paper error-detection benchmark using 220 AI/ML manuscripts and >2,200 controlled synthetic errors, with evidence-grounded peer-review tools. Strong overlap with research-paper auditing and benchmark construction. AuditCal must compare on a *truly comparable subset* and should distinguish authentic errors from synthetic perturbations. https://aclanthology.org/2026.emnlp-main.474/

5. **Luo, Kasirzadeh & Shah (2026), The more you automate, the less you see, PNAS.** Audits AI scientist workflows for improper benchmarks, leakage, metric misuse, selection bias; shows process artifacts (logs/code) improve auditing over final manuscripts alone. This overlaps with evidence/provenance-aware verification; AuditCal cannot claim pioneering process auditing. https://pubmed.ncbi.nlm.nih.gov/42832657/

These references establish relevant prior art, not an exhaustive originality search. Future work must trace citations and inspect implementation and datasets.

## Current AuditCal evidence versus gap

- Actual prototype supports source-aligned *structured* claims, unit tests, explicit unverifiable/abstention outcome, and an independent Python reanalysis path.
- Source-hash-verified genuine AI reports and two public datasets investigated: METR and a pinned Penn State copy of Soccer; original OSF Soccer byte identity remains unverified.
- Stage 11 selected-claim status: **17 supported, 2 flagged source-based count inconsistencies, 4 abstained**, from two newly reanalyzed Claude soccer reports plus a prior Qwen count audit.
- The two Qwen flags concern **distinct player/referee count claims**, not an established p-value/calculation or causal scientific conclusion error.
- Analysis/model association was manually mapped. No automatic free-text extraction benchmark, independent double-labeled ground truth, held-out testing, error rate, or proven algorithmic novelty.
- Source scripts were read as untrusted text; not executed.

## Potential *testable* contribution (NOT yet demonstrated)

**Provenance- and specification-aware numerical claim audit:** given a report, underlying dataset, analysis inclusion rules, and statistical method metadata, decide whether a numerical claim is:

- reproduced under a *matching* specification;
- discrepant under that same specification; or
- not adjudicable because the evidence/method/estimand differs or is unavailable.

The potential distinctive research emphasis is **how to avoid false error flags when analysis paths differ**, with transparent evidence and measured abstention. It is a hypothesis about contribution, not a claim to be first.

## Proposed experimentally answerable questions

- **RQ1: Numerical fidelity:** On independently labeled, held-out claims from real AI-agent reports and controlled erroneous variants, how accurately does AuditCal identify genuine discrepancies versus relevant baselines?
- **RQ2: Specification sensitivity:** On defensible alternative models of the same data, does specification-aware verification reduce false error flags compared with naive numerical comparison and a language-model-only assessor?
- **RQ3: Evidence sufficiency:** How does data/code/model provenance availability affect coverage (fraction adjudicated), false-positive risk, and abstention quality?

## Needed evaluation design, before serious novelty/performance claims

1. Predefine report/dataset inclusion, claim unit, model/estimand identity, acceptance tolerance and failure classes. Avoid choosing only impressive successes.
2. Create a held-out corpus with authentic AI-agent numerical claims; optionally add a *separate* controlled-error set to test sensitivity. Never blend synthetic-error prevalence with authentic error-rate claims.
3. Label source sample/filter, specification, reported figure, independently recomputed result, and adjudication rationale. Obtain independent second reviewer/statistical expert adjudication, and record disagreement.
4. Compare baselines with clear applicability: naive number matching; human/manual independent recomputation; LLM-only verification; statcheck-like arithmetic checking for overlapping NHST statements (statcheck is not directly applicable to every regression and distinct-count claim).
5. Report precision, recall, false-flag rate, coverage/abstention, confidence intervals, model/dataset breakdown, cost, and specification-mismatch robustness. Stratify authentic and synthetic cases.
6. Audit candidate novelty against code/publications and seek professor/statistician feedback; quantify whether any method improvement exceeds baselines.

## Research significance and proposed graduate direction

**Why AuditCal?** To turn the question of trusting AI-generated numerical research claims into a concrete, reproducible pilot. Two real datasets and released agent reports provided both reproducible correct results and source-backed count inconsistencies.

**What did I learn?** Numerical agreement is not the same as scientific validity; model selection, estimand choice, source provenance, uncertainty method, and abstention matter.

**What will I do in a Master's?** Study verification methods for agent-generated statistical claims, design independently labeled evaluations, test model-specification awareness, and compare with existing automated auditors. Specific methodology to be adapted honestly to a prospective supervisor's expertise.

**What NOT to claim:** that AuditCal invented statistical auditing, is already an accurate general-purpose auditor, has peer-reviewed novelty, provides causal conclusions about the Soccer study, or outperforms established tools.


## Decision gate

Before a new statistical exercise, finish a structured literature matrix (research problem / input artifacts / numerical recomputation / method identity / abstention / evaluation method / known limitations), then define one small held-out benchmark. If distinctiveness is not credible, *reposition AuditCal as evidence of research practice rather than force a novelty claim*.
