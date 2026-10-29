# External research sources and attribution

AuditCal contains original source-based analysis and tests about independent externally published datasets and released AI-agent reports. Their authors and rights must not be confused with AuditCal's authorship.

| Referenced external source | Purpose in AuditCal | Public project and observed license (2026-10-29) |
|---|---|---|
| **Amazon Science — Agentic Forking Path**, study associated with Bertran, Fogliato & Wu (2026) | Published AI-agent reports and original scripts inspected as **untrusted text only**; report/source hashes, limited diagnostic excerpts and numerical claims included in evidence metadata. | [Original project](https://github.com/amazon-science/agentic-forking-path). GitHub identifies **Apache-2.0**, with original [LICENSE](https://github.com/amazon-science/agentic-forking-path/blob/main/LICENSE) and [NOTICE](https://github.com/amazon-science/agentic-forking-path/blob/main/NOTICE). **NOTICE:** Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. |
| **METR — Early-2025 AI Experienced Open-Source Developers study** | Independently referenced task-level statistical data and public study methodology. **Raw full dataset is not included in this repository.** | [Original repository](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs) and [study details](https://metr.org). A definitive license identifier **was not confirmed** for this public repository in this audit. Verify before redistributing underlying data or source. |
| **Penn State Psychology — Psych 490 Reproducibility (2024)** | Pinned teaching copy of the public Soccer red-card observational CSV, used by independent scripts; **full CSV not included here**. | [Course repository](https://github.com/psu-psychology/psych-490-reproducibility-2024-fall), identified by GitHub as **CC0-1.0**. Any separate original OSF study or data rights should be verified independently. |
| **Silberzahn et al. crowdstorming study / OSF** | Background provenance of Soccer data; directly fetched original OSF bytes **were not independently verified**. | [Study OSF node](https://osf.io/fv8c3/). This project does not assert original-host byte identity. |
| **ForkSCOPE and related independent academic auditors** | Prior method comparison, methodological caution and dataset checksum corroboration. | See [method-comparison notes](STAGE12B_LITERATURE_COMPARISON_MATRIX.md). No ForkSCOPE source code is redistributed by AuditCal. |

## Reuse and publication boundaries

1. This repository's **own license is not yet chosen**. Do not assume the appearance of source on GitHub automatically licenses it for reuse.
2. This project does not bundle complete external source datasets or execute any arbitrary external AI-authored analysis program.
3. Some pinned evidence snapshots include brief portions of published AI-agent code as **static documentation**, not as AuditCal's own software. Before making this repository broadly public or redistributing those portions, confirm any attribution / included LICENSE / NOTICE requirements of the original Apache-2.0 project.
4. Publication should include reasonable credit to the above original authors and sources, avoid asserting endorsement, and respect any copyright, data-use or privacy conditions of each source.
5. Scientific conclusions and accuracy metrics cannot be inferred merely from license availability or from passing source-reproduction tests.

This document is a source-attribution inventory and **not a legal opinion**.
