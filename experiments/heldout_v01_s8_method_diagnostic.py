"""S8-only inference-method diagnostic on pinned public Soccer source data.

This is a targeted methodological sensitivity investigation, NOT a new held-out
evaluation, gold label, or real-world AuditCal accuracy measurement.
Source AI-authored code is inspected as TEXT; it is never imported or executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
import statsmodels
import statsmodels.api as sm

SOURCE_SHA = "6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"
REPORT_RD_PP = 0.0811
REPORT_CI_PP = [-0.0002, 0.202]


def interval_and_p(estimate: float, se: float) -> dict:
    if se <= 0 or not np.isfinite(se):
        raise ValueError("Invalid marginal effect uncertainty")
    z = float(norm.ppf(.975))
    return {
        "estimate_probability": estimate,
        "estimate_percentage_points": 100 * estimate,
        "se_probability": se,
        "ci_95_percentage_points": [100 * (estimate - z * se),
                                    100 * (estimate + z * se)],
        "p_two_sided_normal": float(2 * norm.sf(abs(estimate / se))),
    }


def analyze(path: Path) -> dict:
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != SOURCE_SHA:
        raise ValueError(f"Source hash mismatch: {digest}")
    d = pd.read_csv(path, low_memory=False)
    skin = d[["rater1", "rater2"]].mean(axis=1, skipna=True)
    good = (skin <= .25) | (skin >= .75)
    needs = ["position", "leagueCountry", "height", "weight",
             "games", "redCards", "playerShort", "refNum"]
    selected = d.loc[good & d[needs].notna().all(axis=1)].copy()
    if len(selected) != 99645:
        raise ValueError("Unexpected S8 frozen sample")
    selected["dark_skin"] = (skin.loc[selected.index] >= .75).astype(int)
    y = np.column_stack([selected.redCards, selected.games - selected.redCards])
    if (y < 0).any():
        raise ValueError("Negative binomial trials")
    x = selected[["dark_skin", "height", "weight", "position", "leagueCountry"]].copy()
    x = sm.add_constant(x)
    x = pd.get_dummies(x, columns=["position", "leagueCountry"],
                       drop_first=True, dtype=float)
    x = x.astype(float)
    with warnings.catch_warnings(record=True) as notice:
        warnings.simplefilter("always")
        fit = sm.GLM(y, x, family=sm.families.Binomial()).fit(
            cov_type="cluster",
            cov_kwds={"groups":selected.playerShort},
            maxiter=100,
        )
    if not bool(fit.converged):
        raise ValueError("S8 independent source-data GLM did not converge")

    design = x.to_numpy()
    beta = np.asarray(fit.params, dtype=float)
    cov = np.asarray(fit.cov_params(), dtype=float)
    idx = list(x.columns).index("dark_skin")
    base = design @ beta
    q = expit(base)
    deriv = float(np.mean(beta[idx] * q * (1-q)))
    grad_der = np.mean(
        (beta[idx] * q * (1-q) * (1-2*q))[:,None] * design,
        axis=0)
    grad_der[idx] += float(np.mean(q * (1-q)))
    se_der = float(np.sqrt(grad_der @ cov @ grad_der))
    x0 = design.copy(); x0[:,idx] = 0
    x1 = design.copy(); x1[:,idx] = 1
    q0 = expit(x0 @ beta)
    q1 = expit(x1 @ beta)
    discrete = float(np.mean(q1-q0))
    grad_dis = np.mean(
        (q1*(1-q1))[:,None]*x1 - (q0*(1-q0))[:,None]*x0,
        axis=0,
    )
    se_dis = float(np.sqrt(grad_dis @ cov @ grad_dis))

    native = {}
    for dummy in (False, True):
        label = "dydx_continuous_derivative" if not dummy else "dydx_dummy_discrete"
        try:
            output = fit.get_margeff(method="dydx", at="overall", dummy=dummy)
            terms = list(x.columns)[1:] if "const" in x.columns else list(x.columns)
            position = terms.index("dark_skin")
            native[label] = {
                "estimate_probability": float(output.margeff[position]),
                "se_probability": float(output.margeff_se[position]),
                "p": float(output.pvalues[position]),
                "ci_95_probability": [float(z) for z in output.conf_int()[position]],
                "note": "Native statsmodels marginal-effect result; independent program called library, not AI source script",
            }
        except Exception as exc:
            native[label] = {"error":type(exc).__name__, "message":str(exc)[:250]}
    mid = sum(REPORT_CI_PP)/2
    symmetry = abs(mid-REPORT_RD_PP)
    answer = {
        "status": "SOURCE_DATA_METHOD_DIAGNOSTIC_SINGLE_RESEARCHER_NOT_GOLD",
        "source_sha256":digest, "dataset":"pinned educational Soccer CSV; OSF-origin SHA externally corroborated",
        "selected_rows":len(selected),
        "model":"binomial trials logit, source-aligned player-cluster covariance",
        "statsmodels":statsmodels.__version__,
        "agent_code_executed":False,
        "regression_converged":True,
        "fit_warnings":[str(x.message) for x in notice],
        "reported":{"rd_percentage_points":REPORT_RD_PP,
                    "ci_95_percentage_points":REPORT_CI_PP,
                    "p_from_report_prose":.051,
                    "source_script_calls":"result.get_margeff(method='dydx', at='overall') with no dummy=True"},
        "own_continuous_derivative_delta":interval_and_p(deriv,se_der),
        "own_binary_0_to_1_discrete_delta":interval_and_p(discrete,se_dis),
        "statsmodels_native_marginal_effects":native,
        "report_ci_symmetry_check":{
            "ci_midpoint_percentage_points":mid,
            "reported_estimate_percentage_points":REPORT_RD_PP,
            "distance_between_ci_midpoint_and_reported_estimate_pp":symmetry,
            "implication":"Published interval is asymmetric about reported point, whereas standard statsmodels marginal-effect conf_int uses symmetric normal/Wald uncertainty around the selected point."
        },
        "gold_label":None,
        "reviewer_needed":True,
        "note":"Compare model, claim, source-code semantics and inference method separately. Do not turn these results into a confirmed scientific reporting-error label.",
    }
    return answer


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--soccer", type=Path, required=True)
    p.add_argument("--output", type=Path,
                   default=Path("results/heldout_v01/s8_method_diagnostic.json"))
    args = p.parse_args()
    evidence = analyze(args.soccer)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8")
    print("S8_METHOD_DIAGNOSTIC",json.dumps(evidence),flush=True)


if __name__=="__main__":
    main()
