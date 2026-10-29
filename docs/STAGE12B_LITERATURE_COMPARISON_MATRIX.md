# Stage 12b — Literature comparison matrix and research positioning
**CSC 2027 / AuditCal | 2026-10-29 | Initial targeted literature scan, not a systematic review**
**Status:** Literature positioning documented. **Novelty, reliability and application readiness NOT established.**

## The question for a prospective Master's supervisor
Can a verification system independently recompute numerical claims from original research data **while aligning the stated statistical specification**, and avoid false error flags when alternative legitimate methods/estimands produce different figures?

This is narrower and more defensible than 'a novel AI scientific fact checker'. It is a *potentially useful research question*, not evidence that the answer/method is new.

## Targeted related-work comparison (direct publication sources)

| Existing work | Core scope (source-based) | Comparison with proposed AuditCal; what we can NOT claim |
|---|---|---|
| **statcheck / Nuijten et al. 2016**, Behavior Research Methods, doi:10.3758/s13428-015-0664-2 | Parses certain APA-style significance-test reports and checks internal p-value consistency using stated test statistics and degrees of freedom, with rounding considerations. | Proves automated statistical inconsistency detection is prior art. AuditCal's candidate distinction is *source-data refitting with model/sample alignment* for specific claims; not a direct drop-in replacement. |
| **CLAIM-BENCH / Javaji et al. 2025**, IJCNLP-AACL, https://aclanthology.org/2025.ijcnlp-long.127/ | Scientific claim/evidence extraction and textual validation across >300 evidence pairs. | Overlaps any future free-text claim extraction. The current AuditCal prototype does **not** yet have measured end-to-end extraction performance. |
| **MuSciClaims 2025**, IJCNLP-AACL, https://aclanthology.org/2025.ijcnlp-long.175/ | Scientific claim verification involving figures and multimodal evidence. | Shows broader scientific claim verification benchmarks exist. AuditCal should not claim first to verify scientific statements. |
| **Miao, Pritchard & Zou, The Agentic Garden of Forking Paths 2026**, https://arxiv.org/abs/2607.01507 | AI-agent analysis choices produce divergent yet often defensible conclusions from the same dataset; Agentic Bootstrap explores multiverse sensitivity. | Central scientific motivation for distinguishing *model/analysis choices* from calculation errors. Our authentic report corpus comes from related public experiment material. Cannot claim to have introduced multiverse-aware reasoning. |
| **ForkSCOPE / Balaji et al. 2026**, https://arxiv.org/abs/2609.12438 | Organizes many AI-generated analysis code paths and surfaces analytic decision forks in a human-AI pipeline. | Potentially overlaps proposed method/provenance-awareness, so originality must be checked against implementation. No comparative experiment has been done. |
| **PaperAudit-Bench / Tu et al. 2026**, EMNLP, https://aclanthology.org/2026.emnlp-main.474/ | Benchmark for research-paper error detection: 220 AI/ML papers, >2,200 controlled synthetic errors; evidence-grounded review generation. | Strong overlap with AI paper auditing/benchmarks. AuditCal could focus on *data- and specification-verified statistical numerical claims* if this offers measured added value. Cannot claim first benchmark. |
| **Luo, Kasirzadeh & Shah 2026**, PNAS, doi:10.1073/pnas.2610214123 | Demonstrates vulnerabilities in AI-scientist workflows and usefulness of logs/code for auditing hidden methodological issues. | Process- and evidence-aware auditing is prior art. AuditCal's claimed distinction, if any, needs quantified comparison rather than generic 'checks source material'. |

**Interpretation caution:** Some systems do not aim to refit numerical models from original datasets; that is a *scope difference*, not proof AuditCal is superior or novel. Table is a targeted scan, not exhaustive citation tracing or code audit.

## What Stage 7–11 actually demonstrates
- Reproducible Python checker for **structured, manually mapped** claims, with explicit abstention.
- Independently recomputed selections from genuine AI-agent reports on METR and Soccer (Soccer data = pinned teaching copy; original OSF byte identity pending).
- Stage 11: **17 supported, 2 flagged, 4 abstained** selected source-matched claims, combining new Claude regression replication with prior Qwen count checks.
- Two flags are incorrect **reported distinct entity counts** in one real Qwen report. They do NOT prove erroneous regression significance, a false causal conclusion, or a generalizable model error rate.
- No held-out, independently adjudicated evaluation, extraction precision/recall, formal statistical performance estimate, baseline superiority, or confirmed novel algorithm.

## Literature-gap judgment
**Already occupied:** statistical consistency checking, LLM claim/evidence validation, scientific paper auditing, AI-scientist process auditing, analysis-fork visualization.

**Candidate niche, unproven:** evaluate a transparent, *sample/model/estimand-aligned* original-data numerical verifier with principled abstention specifically under method differences, and quantify whether this decreases false accusations compared with naive number matching and an LLM-only auditor.

**Not yet established:** that there is an unmet gap that no competing system already addresses, or that our software solves it better.

## Supervisor-facing research questions (proposals, not results)
- **RQ1** How accurately can source-data numerical checking detect real AI-agent reporting inconsistencies when dataset, filters and statistical model are matched?
- **RQ2** Does method/estimand alignment reduce false-discrepancy flags on alternative defensible analysis paths versus naive numerical comparisons?
- **RQ3** How should the checker abstain when provenance, sample selection or inference procedure is insufficiently specified, and what is the coverage/accuracy tradeoff?

## Next actions (no random tests)
1. Inspect source code/methods for the 3 closest comparators: statcheck, PaperAudit-Bench and process-auditing methods; add a *feature-based* comparison rather than superficial titles.
2. Prespecify a **small held-out pilot** with authentic claims, negative controls and documented alternatives; separate authentic claims from deliberately perturbed examples. Avoid using the 23 previously selected examples as fresh held-out cases.
3. Define independent adjudication with a second reviewer, exact same-sample/method matching criteria, and flags vs abstentions.
4. Compare baselines only on overlapping tasks (naive value matching; LLM-only review; arithmetic checks where applicable), and report false-flag rate, precision/recall, coverage and limitations.
5. In parallel, assemble CSC 2027 research CV, proposal and professor-fit map rather than delaying all application work until full scientific publication.

## Honest decision for the student
The initial AuditCal software and exploratory cross-dataset replication are **ready as a portfolio research prototype**. A manuscript-grade, independently validated method is **not complete**. Professor outreach remains on hold until scholarship profile and evidence-backed draft are assessed.

**One-sentence interview framing:** 'I built a reproducible pilot to investigate whether AI-generated statistical numbers can be independently checked; the experiments taught me that validating a result also requires matching the dataset, statistical specification and uncertainty method, so I want to study verification systems that catch genuine mistakes without mislabeling defensible alternative analyses.'

---

## 2026-10-29 implementation-aware follow-up (adds NEW source/code evidence; not a new independent research stage)

**Purpose:** The earlier matrix compared paper titles and documented scopes. This follow-up inspected concrete publicly released functions/modules, plus AuditCal's actual core, to establish a fairer boundary. **No new statistical experiments were run. No head-to-head benchmark was run.**

### Examined source snapshots, read as text only
- **statcheck** public code at commit `db9c9d3ed0b6b0aeda26c0612cbecf5912e1092c` (2026-10-26), [`R/compute_p.R`](https://github.com/MicheleNuijten/statcheck/blob/db9c9d3ed0b6b0aeda26c0612cbecf5912e1092c/R/compute_p.R) and [`R/error_test.R`](https://github.com/MicheleNuijten/statcheck/blob/db9c9d3ed0b6b0aeda26c0612cbecf5912e1092c/R/error_test.R), plus [package FAQ](https://statcheck.io/) and [CRAN documentation](https://search.r-project.org/CRAN/refmans/statcheck/html/statcheck.html).
- **PaperAudit** public code at commit `de7582b188ca2d867298de978386ec1f5085806f` (2026-09-16), [`detect/README.md`](https://github.com/TU2021/PaperAudit/blob/de7582b188ca2d867298de978386ec1f5085806f/detect/README.md), [`detect/agents.py`](https://github.com/TU2021/PaperAudit/blob/de7582b188ca2d867298de978386ec1f5085806f/detect/agents.py) and [`detect/mas_error_detection.py`](https://github.com/TU2021/PaperAudit/blob/de7582b188ca2d867298de978386ec1f5085806f/detect/mas_error_detection.py), plus [EMNLP paper](https://aclanthology.org/2026.emnlp-main.474/).
- **Process-auditing comparator:** [Luo et al., PNAS 2026 full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13663820/); compared methodology as reported in the article, **not the full companion source implementation**.
- **AuditCal:** current [`src/auditcal/core.py`](https://github.com/ds-aziz/CSC2027-AuditCal/blob/auditcal-starter-v0-1/src/auditcal/core.py) and Stage 11 independently authored Soccer scripts. No external-agent script was executed in this review.

### Actual capability boundaries (source checked, not experimental performance)

| Dimension | statcheck (source checked) | PaperAudit-Bench / PaperAudit (source checked) | Luo et al. workflow auditing (article checked) | AuditCal CURRENT implementation |
|---|---|---|---|---|
| **Primary input** | Article/text containing APA-style NHST results | Parsed paper blocks/JSON, sections, multimodal evidence, optional web retrieval | Final paper vs agent code/execution logs and controlled failure cases | **Manually structured claim records** + externally computed evidence |
| **Checking computation** | Recomputes p from **reported** test statistics and df with R distributions; checks rounding bounds | Multi-agent LLM plans, retrieves, reviews and merges suspected errors | LLM-based auditing/classification of methodological pitfalls using paper/logs/code | Python core numeric equality/tolerance and type checks; **separate researcher-written scripts** independently refit certain datasets/models |
| **Uses original dataset to refit regression?** | **Not its stated/implemented standard NHST consistency workflow** | **Not established in the inspected detection path**; do NOT claim an exhaustive absence from all modules | Not the main classifier described; paper studies workflow artifacts and controlled conditions | **Only where a case-specific independent experiment script has been written**; NOT generic, automatic source-data ingestion/refit |
| **Explicit model/sample/estimand safeguard?** | Supports appropriate NHST/rounding/tail checks; not cross-regression-data model provenance matching | Cross-document contextual reasoning but **no verified deterministic same-estimand gate in inspected functions** | Studies methodological decision/pitfall provenance; overlaps method-aware scientific oversight | Core abstains when caller's `model_id` and `evidence_model_id` differ; **IDs assigned manually**, not automatically proven semantic equivalence |
| **Abstention and error handling** | Does not flag incompatible/undetected APA results as verified; supports rounding and one-tailed distinctions | LLM findings and subsequent evaluation/adjudication, with evidence descriptions | Detects process pitfalls by paper-vs-artifacts; article reports classification metrics | Explicit `UNVERIFIABLE` on missing provenance, unsupported or causally unjustified claims, mismatched model ID; current policy is rule-based |
| **Demonstrated evaluation** | Published method and usage; not tested in this AuditCal exercise | Published corpus of **220 papers, >2,200 controlled synthetic errors** with detection evaluation | Balanced controlled pitfalls and paper-only vs full-artifact auditor experiments | **None on a held-out independently gold-labeled set**; 23 hand-mapped selected Soccer claims are not benchmark metrics |

**Code-specific observations:**
- `statcheck::compute_p` calculates p-values for t, F, Z, r, chi-square and Q using R probability functions. `error_test` explicitly checks p-value ranges permitted by **rounding of the reported test statistic**. Thus simply adding a tolerance to AuditCal is **not an innovation**.
- PaperAudit detection architecture explicitly includes planner/retriever/specialist, optional web retrieval, multimodal section/context review, merging, and an LLM-based ground-truth matching evaluation; AuditCal cannot claim to be first to make evidence-aware or agent-based scientific audit.
- The Luo et al. study reports strong benefit from access to source process/logs/code over final manuscript alone; **method/provenance awareness is already a studied idea**.
- In AuditCal `core.py`, the `verified` number is passed **by caller**, and `model_id == evidence_model_id` is a **string equality check** rather than automated inference of matching data filters, transformations, statistical models or estimands. The Stage 11 independent source-data recomputation is case-specific external Python, not a general end-to-end auditing pipeline.

### Revised originality judgment and falsifiable next decision
**Unsupported novelty claims to reject:** 'first AI research checker', 'first automated p-value verifier', 'first use of evidence/provenance in scientific auditing', or 'already fully automatic source-data verification'.

**Candidate gap, still unproven:** a narrowly scoped, reproducible evaluator that **independently matches data/sample/model/estimand metadata to numeric claims**, explicitly abstains when alignment cannot be demonstrated, and measures false-alarm reduction against real alternative analysis paths. Achieving this requires genuinely implementing/validating stronger semantic specification matching than the current manually entered IDs.

**Most relevant next NEW work:** pre-register a small held-out evaluation protocol (not yet execute it); clearly separate real agent reports vs controlled mutations; construct and independently adjudicate sample/model/estimand labels; use a *naive numeric matcher* and an *LLM-only assessor* as applicable baselines. Use `statcheck` only for true overlapping APA-style NHST examples, not for distinct counts or fitted odds ratios with unavailable reported statistics. First candidate question: **How much does explicit specification matching decrease the false-flag rate on genuinely different-but-valid statistical methods?**

**Additional research still open:** Code-level review of ForkSCOPE and the PNAS auditing implementation, backward/forward citation tracing, held-out experiment, and independent review. **Do not declare novelty confirmed or literature review exhaustive.**


---

## 2026-10-29 deeper implementation check: ForkSCOPE + origin study (in-place continuation, not another literature stage)

**Why reviewed:** This is one of the previously OPEN close comparators, not a repeat of the existing seven-paper title matrix. The original corpus used for AuditCal pilot came from the Bertran et al. AI-analyst research; the same artifacts are analyzed by ForkSCOPE. These projects are therefore especially relevant to our originality boundary.

**Exact sources inspected:**
- ForkSCOPE authors' [paper](https://arxiv.org/abs/2609.12438) and GitHub [README](https://github.com/TZstats-Columbia/ForkSCOPE/blob/d55603c3b2e58205885aba1ddaf4738a9cf38679/README.md), [docs/WORKFLOW.md](https://github.com/TZstats-Columbia/ForkSCOPE/blob/d55603c3b2e58205885aba1ddaf4738a9cf38679/docs/WORKFLOW.md), [scripts/distill.py](https://github.com/TZstats-Columbia/ForkSCOPE/blob/d55603c3b2e58205885aba1ddaf4738a9cf38679/scripts/distill.py), [scripts/check_outcomes.py](https://github.com/TZstats-Columbia/ForkSCOPE/blob/d55603c3b2e58205885aba1ddaf4738a9cf38679/scripts/check_outcomes.py) and [docs/AUDITING.md](https://github.com/TZstats-Columbia/ForkSCOPE/blob/d55603c3b2e58205885aba1ddaf4738a9cf38679/docs/AUDITING.md), commit \`d55603c3b2e58205885aba1ddaf4738a9cf38679\` (2026-09-11). Code inspected **as text, not executed**.
- Bertran, Fogliato & Wu, [PNAS 2026 original paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13393493/) (DOI 10.1073/pnas.2606495123), which provides the public AI-agent corpora that AuditCal is checking. This paper documents a transcript-aware LLM auditor and known methodology/estimand compliance screening.

### Verified overlaps (cannot claim originality for these)

| Feature / scientific purpose | Existing evidence | Consequence for AuditCal wording |
|---|---|---|
| **Line-anchored code ↔ prose checking** | ForkSCOPE \`scripts/distill.py\` segments code/prose, links claims to code decisions, detects silent choices and misalignments. | **Not a novel idea from AuditCal**. S5's mismatch between a written formula and narrative is an example of a broader already studied class. |
| **Method choices and valid variation** | ForkSCOPE induces forks/options from scripts, not a fixed taxonomy; Bertran et al. compare varied plausible analysis pipelines and fixed prespecified estimands. | **Not original** to notice valid alternatives or build a method-sensitive audit concept. |
| **Evidence provenance, machine-auditable workflows, audit abstention / human escalation** | ForkSCOPE retains source spans and unreviewed gaps, builds audit artifacts and human review gates; its \`check_outcomes.py\` even reports missing fragments as unverified instead of inventing provenance. | Do NOT claim 'first provenance-aware', 'first evidence-linked auditor' or 'first to abstain' as our contribution. |
| **AI auditor screens analysis correctness** | Bertran et al. document transcript-based Sonnet auditor checks including estimand alignment and uncertainty quantification. | Do NOT claim an auditor of AI analyst results is unique or that the underlying released original reports had no auditing. |
| **Numerical output linkage** | ForkSCOPE \`scripts/check_outcomes.py\` checks outcome records against recorded per-run fragments; its audit layers evaluate claims/derived maps. | A provenance and fragment-consistency checker already exists; **avoid implying ForkSCOPE checks nothing numeric**. |
| **Independent original-data same-specification recomputation as a generic product** | **Not demonstrated by the handful of inspected ForkSCOPE scripts**; AuditCal has only case-specific independently authored METR/Soccer reanalysis, not general source-code-to-model semantic automation. | **Candidate empirical task distinction, NOT a proved uncovered literature gap or completed feature**. |

**One particularly useful adverse finding:** ForkSCOPE's original author README reports a comparison against a pinned copy of the **same** \`amazon-science/agentic-forking-path\` corpus. AuditCal's 8 reports are therefore not unique, unstudied scientific material globally. They are **previously uninspected BY OUR pilot under its frozen selection**, not virgin to all published researchers.

### Updated candidate positioning — narrower and falsifiable

> **Potential Master's research question:** Under a fixed *source-data, sample, model and estimand* contract, can independent numerical recomputation plus explicit abstention reduce wrong numerical-discrepancy accusations compared with a values-only checker, without giving up too much coverage? How can a verifier recognize when the contract cannot be established rather than inventing equivalence?

This is still a **hypothesis and evaluation plan**, not an established novel method. Reporting an algorithm that autonomously identifies this full contract would require actually implementing and validating semantic source/method matching; current AuditCal only checks caller-provided model IDs.

### Close-comparator review status
- **Done:** Detailed code-anchored scope review of statcheck, PaperAudit's detector, and **ForkSCOPE**, plus original Bertran AI-auditor paper.
- **Partial:** Luo et al. AI workflow audit reviewed from paper, not independently inspected companion implementation; related work citations not systematic/exhaustive.
- **Still decisive scientifically:** An independent dataset-level and report-level gold-labeled baseline comparison; review of ambiguity cases and measured false-positive/abstention trade-offs. **Novelty not proven**; a strong research proposal may present this as a question, not an established gap.

**No new tests run, no code modified, no new benchmarks produced in this comparison.**
