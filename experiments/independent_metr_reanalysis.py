"""Independently re-estimate a released AI-agent analysis using primary METR data.

Security: NEVER execute the agent-authored final_analysis.py. This script is
human-specified from the reported model equations and public METR dataset.

No universal validity claims; note model/SE choices and missing-data assumptions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels as sm
import statsmodels.formula.api as smf

SOURCE_URL = (
    "https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/"
    "blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv"
)
AGENT_SOURCE_URL = (
    "https://github.com/amazon-science/agentic-forking-path/tree/main/"
    "experiment_data/workspaces/standard/"
    "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/"
    "sample_metr/2025-11-12T17-17-32%2B0000"
)
# Numbers are transcribed from the independently obtained public report,
# not claimed to be our results.
AGENT_REPORTED = {
    "primary": {"n": 246, "developers": 16, "gmr": 1.1570,
                "p_value": 0.0658, "pct_ci": [-0.95, 35.15]},
    "secondary": {"n": 230, "developers": 16, "gmr": 1.201,
                  "p_value": 0.0382, "pct_ci": [1.15, 42.64]},
}
# Loose audit thresholds account for small implementation/version differences,
# not pre-registered scientific rejection boundaries.
TOLERANCE_GMR = 0.02
TOLERANCE_P = 0.01
TOLERANCE_PCT_CI_PP = 3.0


def describe_fit(fit: Any, n: int, developers: int, method: str) -> dict[str, Any]:
    beta = float(fit.params["ai_treatment"])
    se = float(fit.bse["ai_treatment"])
    pvalue = float(fit.pvalues["ai_treatment"])
    ci = np.asarray(fit.conf_int().loc["ai_treatment"], dtype=float)
    gm = float(np.exp(beta))
    out = {
        "method": method,
        "n": int(n),
        "developers": int(developers),
        "beta_log": beta,
        "se_log": se,
        "p_value": pvalue,
        "ci_log": [float(x) for x in ci],
        "gmr": gm,
        "pct_time_change": (gm - 1) * 100,
        "pct_ci": [float((np.exp(x) - 1)*100) for x in ci],
    }
    if hasattr(fit, "converged"):
        out["converged"] = bool(fit.converged)
    return out


def compare_one(actual: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    diffs = {
        "gmr": actual["gmr"] - expected["gmr"],
        "p_value": actual["p_value"] - expected["p_value"],
        "pct_ci": [a - b for a, b in zip(actual["pct_ci"], expected["pct_ci"])],
    }
    sample_match = (actual["n"] == expected["n"]
                    and actual["developers"] == expected["developers"])
    numerical_match = (
        abs(diffs["gmr"]) <= TOLERANCE_GMR
        and abs(diffs["p_value"]) <= TOLERANCE_P
        and all(abs(x) <= TOLERANCE_PCT_CI_PP for x in diffs["pct_ci"])
    )
    has_valid_fit = actual.get("converged", True)
    status = ("CONSISTENT_WITH_REPORTED_ANALYSIS"
              if sample_match and numerical_match and has_valid_fit
              else "DIFFERENCE_REQUIRES_INVESTIGATION")
    return {
        "status": status,
        "sample_size_matches": sample_match,
        "numerical_agreement_within_declared_tolerances": numerical_match,
        "fit_converged": has_valid_fit,
        "differences_actual_minus_reported": diffs,
        "agreement_is_not_proof_of_scientific_validity": True,
    }


def independently_reanalyse(path: Path) -> dict[str, Any]:
    bytes_ = path.read_bytes()
    df = pd.read_csv(path)
    needed = {
        "dev_id", "ai_treatment", "predicted_time_no_ai",
        "initial_implementation_time", "post_review_implementation_time"
    }
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected public METR columns: {sorted(missing)}")
    if df[list(needed - {"post_review_implementation_time"})].isna().any().any():
        raise ValueError("Missing nonoptional primary values")
    if (df["initial_implementation_time"] <= 0).any():
        raise ValueError("Initial implementation time must be strictly positive for log model")
    if (df["predicted_time_no_ai"] <= 0).any():
        raise ValueError("Task-size estimates must be positive for log model")
    if not df["ai_treatment"].isin([0, 1]).all():
        raise ValueError("Unexpected treatment values")

    d = df.copy()
    d["log_initial_time"] = np.log(d["initial_implementation_time"])
    d["log_task_size"] = np.log(d["predicted_time_no_ai"])

    # Independently implement equations from the published AI report.
    mixed = smf.mixedlm(
        "log_initial_time ~ ai_treatment + log_task_size",
        data=d,
        groups=d["dev_id"],
    ).fit(reml=True)
    primary = describe_fit(
        mixed, len(d), d["dev_id"].nunique(),
        "REML random-intercept mixed-effects regression; Wald normal test"
    )

    d2 = d.dropna(subset=["post_review_implementation_time"]).copy()
    d2["total_time"] = d2["initial_implementation_time"] + d2["post_review_implementation_time"]
    if (d2["total_time"] <= 0).any():
        raise ValueError("Nonpositive total time for secondary log model")
    d2["log_total_time"] = np.log(d2["total_time"])
    # statsmodels' cluster estimator uses developer clusters; inference with
    # Student t G-1 degrees of freedom (16 developers -> df 15).
    secondary_fit = smf.ols(
        "log_total_time ~ ai_treatment + log_task_size", data=d2
    ).fit(cov_type="cluster", cov_kwds={"groups": d2["dev_id"], "use_correction": True},
          use_t=True)
    secondary = describe_fit(
        secondary_fit, len(d2), d2["dev_id"].nunique(),
        "OLS with developer-clustered standard errors, t_15 inference"
    )
    # Avoid treating implementation warnings as trustworthy evidence.
    out = {
        "source_dataset": SOURCE_URL,
        "source_agent_report": AGENT_SOURCE_URL,
        "dataset_sha256_downloaded_bytes": hashlib.sha256(bytes_).hexdigest(),
        "dataset_is_primary_release": True,
        "original_agent_script_was_executed": False,
        "dataset_rows": len(df),
        "software_versions": {"statsmodels": sm.__version__, "pandas": pd.__version__},
        "comparison_tolerances": {
            "gmr_absolute": TOLERANCE_GMR,
            "p_value_absolute": TOLERANCE_P,
            "ci_endpoint_percentage_points": TOLERANCE_PCT_CI_PP,
        },
        "primary": {"reported": AGENT_REPORTED["primary"], "recomputed": primary,
                    "audit": compare_one(primary, AGENT_REPORTED["primary"])},
        "secondary": {"reported": AGENT_REPORTED["secondary"], "recomputed": secondary,
                      "audit": compare_one(secondary, AGENT_REPORTED["secondary"])},
        "independent_statistical_conclusions_count": 2,
        "notes": (
            "Numerical reproduction only for two reported estimands. This does not "
            "prove the statistical design, random-effects assumptions, handling "
            "of missing data, or causal statements are valid. A different "
            "defensible specification may produce other results."
        ),
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Independently recompute METR agent results")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--out", type=Path, default=Path("results/metr_independent_reanalysis.json"))
    args = parser.parse_args()
    out = independently_reanalyse(args.dataset)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    statuses = [out[k]["audit"]["status"] for k in ("primary", "secondary")]
    if not all(x == "CONSISTENT_WITH_REPORTED_ANALYSIS" for x in statuses):
        # Fail loudly so that differences are not silently declared "correct".
        raise SystemExit("At least one reported estimand differs; review model assumptions")

if __name__ == "__main__":
    main()
