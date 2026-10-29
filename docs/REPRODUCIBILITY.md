# AuditCal — Reproduce the software checks and bounded public-data investigations

This guide distinguishes **self-contained software checks** from optional source-data reanalysis. It does not claim to revalidate the original study scientifically.

## Run the self-contained software

Requires Python 3.10+ and an internet connection when installing dependencies.

```bash
python -m pip install -e '.[test]'
python -m pip install -r requirements-experiments.txt
python -m pytest -q
python -m auditcal.cli examples/claims.jsonl
python -m experiments.stage10_audit_verified_count_claims
python -m experiments.audit_authentic_metr_claims
```

The last two commands read **checked-in historical numerical snapshots**; they **do not** download or independently refit original source datasets. The tests include both synthetic unit cases and fixed snapshot checks; the test pass count is not a system accuracy estimate. The held-out evaluation scorer must remain **blocked until two genuine independent reviewers and paired predictions exist**.

## Optional fresh source-data calculations (requires external source files)

**METR:** use the pinned original published public dataset `data_complete.csv` at commit `7ff2d7670235f531dff77eff58355bd77392f396` of [METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs). Expected SHA-256: `1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746`.

```bash
python -m experiments.heldout_v01_metr_inference --metr /path/to/data_complete.csv
python -m experiments.heldout_v01_s5_s6_method_diagnostic --metr /path/to/data_complete.csv
```

**Soccer:** use the pinned Penn State teaching CSV `src/surveys/csv/CrowdstormingDataJuly1st.csv` at commit `b35582ee3f2bb4ee2cc8986a0a878081fbad495d` of [psu-psychology/psych-490-reproducibility-2024-fall](https://github.com/psu-psychology/psych-490-reproducibility-2024-fall). Expected SHA-256: `6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a`.

```bash
python -m experiments.heldout_v01_soccer_inference --soccer /path/to/CrowdstormingDataJuly1st.csv
python -m experiments.heldout_v01_s8_method_diagnostic --soccer /path/to/CrowdstormingDataJuly1st.csv
python -m experiments.stage10_soccer_source_count_audit /path/to/CrowdstormingDataJuly1st.csv
```

The Stage10 source count program fetches **only original report/script text**, checks their published SHA-256 signatures, and **does not execute the agent-authored script**. Original publications and redistributable rights belong to their owners. Do not upload protected raw data without permission.

## Evidence interpretation and limitations

- Case-specific figures and prior source-backed reports: [preliminary readout](../evaluation/HELDOUT_V01_PRELIMINARY_READOUT.md) and [Stage10 count finding](STAGE10_SECOND_DATASET_REAL_AI_COUNT_DISCREPANCIES.md).
- Original research workflow run IDs recorded in historical JSON snapshots and some older documents belong to a **private** research archive; a new viewer cannot open those logs. The snapshots and code here are accessible with this repository, but external reanalysis is the route to fresh verification.
- Earlier source reproductions used particular software versions, including versions of `statsmodels`; differing numerical environments may affect borderline confidence interval rounding. Do not silently relax the frozen comparison specification.
- Soccer original OSF file bytes were **not independently retrieved from the original OSF host**, despite independent corroboration of the public teaching copy checksum and size.
- No qualified independent double-reviewed adjudicated 24-case gold labels or valid AuditCal-versus-baseline performance statistic exist.
