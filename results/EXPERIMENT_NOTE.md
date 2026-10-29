# US macrodata experiment: what was actually done

The experiment loads the public `statsmodels.datasets.macrodata` data (203 observations), fits an OLS regression of `realcons` on `realdpi` and `unemp` with HC3 heteroskedasticity-robust covariance, and independently recomputes the structured numerical evidence to which AuditCal compares *15 manually authored* reported claims. It also fits a second legitimate model (`realcons ~ realdpi`) and abstains rather than declaring an error when the model specifications differ.

**Observed in this run:** 6 manually authored correct claims marked supported; 6 intentionally erroneous claims flagged; 3 cases abstained (different specification, causal interpretation, missing numeric evidence). Thus 15/15 *self-authored demonstration expectations* matched. This is not a measure of performance on independent, real AI-generated statistical analyses and **not a scientific generalization**.

Genuine AI-agent traces tested: **0**. Independent annotations: **0**. Published baseline comparisons: **0**. No novel scientific contribution is established. The core engine still relies on structured claims and model labels supplied by a caller; this experiment provides numbers by recomputing models, but it does not parse natural-language AI outputs or independently establish whether a reported model description is authentic.

Reproduce:

```bash
python -m pip install -e '.[test]'
python -m pip install -r requirements-experiments.txt
python experiments/real_data_validation.py
python -m pytest -q
```

Outputs: `results/macrodata_ols_hc3_rows.json` and `results/macrodata_ols_hc3_summary.json`.
