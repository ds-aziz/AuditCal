"""Synthetic arithmetic/formula tests only; no real experimental validation."""
from decimal import Decimal
import numpy as np
import pandas as pd
import patsy
from experiments.heldout_v01_s5_s6_method_diagnostic import frozen_rounding_check


def test_rounding_inside_boundary():
    x = frozen_rounding_check("0.990", "0.9904973579860092")
    assert x["passes_frozen_display_rule"]
    assert x["decimal_places"] == 3


def test_rounding_outside_boundary_without_posthoc_tolerance_change():
    x = frozen_rounding_check("1.351", "1.351514053588001")
    assert not x["passes_frozen_display_rule"]
    assert Decimal(x["difference_beyond_half_unit"]) > Decimal("0.00000001")


def test_one_decimal_percent_is_near_but_inside_rounding_rule():
    x = frozen_rounding_check("10.9", "10.949740182293667")
    assert x["passes_frozen_display_rule"]
    assert Decimal(x["difference_beyond_half_unit"]) == 0


def test_patsy_bitwise_or_is_extra_fixed_predictor_on_tiny_artificial_data():
    # This verifies grammar only. It does NOT execute any AI-authored script.
    d = pd.DataFrame({
        "dev_id": [0,1,2,3,4,5,6,7],
        "ai_treatment": [0,1,1,0,0,1,0,1],
        "predicted_time_no_ai": np.linspace(2,9,8),
    })
    literal = patsy.dmatrix(
        "ai_treatment + predicted_time_no_ai + (1 | dev_id)", data=d, return_type="dataframe"
    )
    intended = patsy.dmatrix(
        "ai_treatment + predicted_time_no_ai", data=d, return_type="dataframe"
    )
    extra = [name for name in literal.columns if name not in intended.columns]
    assert len(extra)==1
    assert np.array_equal(literal[extra[0]].to_numpy(), np.bitwise_or(1,d.dev_id))
