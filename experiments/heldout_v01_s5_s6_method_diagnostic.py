"""Focused S5 source-formula semantics and S6 frozen rounding-boundary audit.

Read-only use of official SHA-pinned METR data. NO original AI-authored program
is executed, NO statistical models are refitted in this diagnostic, and NO
gold labels are assigned. Reuses numerical evidence ALREADY computed by a
separate independent research pipeline (see frozen evidence run URL).
"""
from __future__ import annotations
import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import numpy as np
import pandas as pd
import patsy

METR_SHA = "1493fc46dc379b15d2c39273fa7a7ee98767ff0d90dea113f300d7338f165746"
PREVIOUS_INDEPENDENT_RUN = "https://github.com/ds-aziz/CSC2027-AuditCal/actions/runs/40856299523"
FROZEN_ROUNDING_MARGIN = Decimal("0.00000001")

# Already-documented numbers, NOT newly re-fitted here. Kept at full precision
# from a successful previous independently implemented statistical calculation.
S5_PRIOR = {
    "reported_percent": "10.9",
    "literal_formula_percent": "10.949740182293667",
    "intended_model_percent": "11.802433338484985",
    "reported_gmr": "1.109",
    "literal_formula_gmr": "1.1094974018229367",
    "intended_model_gmr": "1.1180243333848499",
    "reported_ci": ["0.941", "1.308"],
    "literal_formula_ci": ["0.9413427657154363", "1.307689961069896"],
    "intended_model_ci": ["0.9488098702676703", "1.3174171656624993"],
    "reported_p": "0.215",
    "literal_formula_p": "0.2153043028889472",
    "intended_model_p": "0.1827296060914797",
}
S6_PRIOR = {
    "reported_ci": ["0.990", "1.351"],
    "independent_ci": ["0.9904973579860092", "1.351514053588001"],
    "source_code_ci_expression": "np.exp(result_primary.conf_int().loc['ai_treatment'])",
}


def frozen_rounding_check(reported: str, independent: str) -> dict:
    """Check the original fixed report precision; do not tune tolerances."""
    r = Decimal(reported)
    v = Decimal(independent)
    decimal_places = max(0, -r.as_tuple().exponent)
    half = Decimal("0.5") * (Decimal("10") ** (-decimal_places))
    residual = abs(v-r)
    allowed = half + FROZEN_ROUNDING_MARGIN
    return {
        "reported": reported,
        "independent": independent,
        "decimal_places": decimal_places,
        "abs_difference": str(residual),
        "half_display_unit": str(half),
        "frozen_margin": str(FROZEN_ROUNDING_MARGIN),
        "difference_beyond_half_unit": str(max(Decimal("0"), residual-half)),
        "passes_frozen_display_rule": residual <= allowed,
        "conclusion_rule_only": "NUMERICALLY_MATCHES_FROZEN_PRECISION"
            if residual <= allowed else "NUMERICALLY_OUTSIDE_FROZEN_PRECISION",
    }


def check_dataset_and_formula(path: Path) -> dict:
    with path.open("rb") as fh:
        digest = hashlib.file_digest(fh, "sha256").hexdigest()
    if digest != METR_SHA:
        raise ValueError("Official METR SHA-256 source mismatch")
    df = pd.read_csv(path)
    if len(df)!=246 or df["dev_id"].nunique()!=16:
        raise ValueError("METR data identity/structure changed")
    if not pd.api.types.is_integer_dtype(df["dev_id"]):
        raise ValueError("Cannot prove bitwise semantics for noninteger developer IDs")
    # This independently tests formula factor construction only. It neither
    # loads nor runs the AI-produced Python analysis program.
    literal = patsy.dmatrix(
        "ai_treatment + predicted_time_no_ai + (1 | dev_id)",
        data=df, return_type="dataframe",
    )
    intended = patsy.dmatrix(
        "ai_treatment + predicted_time_no_ai",
        data=df, return_type="dataframe",
    )
    extra = [name for name in literal.columns if name not in intended.columns]
    if len(extra)!=1:
        raise ValueError("Unexpected extra term in Patsy literal design")
    x = literal[extra[0]].to_numpy()
    expected = np.bitwise_or(1, df["dev_id"].astype("int64").to_numpy())
    exact = bool(np.array_equal(x, expected))
    if not exact:
        raise ValueError("Original formula was NOT shown to equal 1 OR developer IDs")
    return {
        "official_source_sha256":digest,
        "rows":len(df),
        "developers":int(df.dev_id.nunique()),
        "dev_id_dtype":str(df.dev_id.dtype),
        "patsy_version":patsy.__version__,
        "original_report_formula_as_text":"np.log(initial_implementation_time) ~ ai_treatment + predicted_time_no_ai + (1 | dev_id)",
        "original_source_group_arg_as_text":"groups=df['dev_id']",
        "literal_design_columns":list(literal.columns),
        "prose_intended_design_columns":list(intended.columns),
        "extra_design_columns":extra,
        "extra_column_matches_1_bitwise_or_dev_id":exact,
        "extra_column_distinct_values":sorted(set(int(v) for v in expected)),
        "interpretation":"Formula includes unintended extra FIXED predictor from bitwise OR; separate groups argument provides actual random intercept. No original AI program executed.",
    }


def run(path: Path) -> dict:
    s5_formula = check_dataset_and_formula(path)
    s5_rounding = {
        "percent": frozen_rounding_check(S5_PRIOR["reported_percent"],S5_PRIOR["literal_formula_percent"]),
        "gmr": frozen_rounding_check(S5_PRIOR["reported_gmr"],S5_PRIOR["literal_formula_gmr"]),
        "ci_lower": frozen_rounding_check(S5_PRIOR["reported_ci"][0],S5_PRIOR["literal_formula_ci"][0]),
        "ci_upper": frozen_rounding_check(S5_PRIOR["reported_ci"][1],S5_PRIOR["literal_formula_ci"][1]),
        "p": frozen_rounding_check(S5_PRIOR["reported_p"],S5_PRIOR["literal_formula_p"]),
    }
    s6_rounding = [
        frozen_rounding_check(r,v)
        for r,v in zip(S6_PRIOR["reported_ci"],S6_PRIOR["independent_ci"])
    ]
    return {
        "status":"FOCUSED_SINGLE_RESEARCHER_FORMULA_AND_ROUNDING_DIAGNOSTIC_NOT_GOLD",
        "original_ai_program_executed":False,
        "statistical_models_refitted":False,
        "sample_selection_changed":False,
        "previous_independent_fit_source":PREVIOUS_INDEPENDENT_RUN,
        "frozen_rounding_rule":"nearest half display unit plus <= 1e-8 fixed margin",
        "S5":{"patsy_semantics":s5_formula,"published_vs_literal_rounding":s5_rounding,
              "prior_fit_numbers":S5_PRIOR,
              "issue":"Published numbers match a literal extra fixed covariate; intended prose model gives different effect, CI and p. Requires real expert review."},
        "S6":{"published_vs_independent_ci_rounding":s6_rounding,
              "prior_fit_numbers":S6_PRIOR,
              "issue":"Upper endpoint lies >1e-8 outside frozen nearest-three-decimal rounding interval for reported 1.351; numerical/optimizer version causes still require qualified review."},
        "evidence_boundary":"No second human review; all six previously uncertain claims remain unadjudicated and AuditCal has no validated accuracy metric.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--metr", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("results/heldout_v01/s5_s6_method_rounding.json"))
    args = p.parse_args()
    result = run(args.metr)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("S5_S6_METHOD_DIAGNOSTIC",json.dumps(result),flush=True)

if __name__=="__main__":
    main()
