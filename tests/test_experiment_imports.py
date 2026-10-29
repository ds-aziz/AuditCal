"""Verify every included research experiment's Python imports resolve in this snapshot.

This is a structural smoke test, NOT an execution of any downloaded AI agent code.
"""
import importlib
import pytest

MODULES = [
    "experiments.audit_authentic_metr_claims",
    "experiments.heldout_v01_count_evidence",
    "experiments.heldout_v01_filtered_soccer_counts",
    "experiments.heldout_v01_metr_inference",
    "experiments.heldout_v01_s5_s6_method_diagnostic",
    "experiments.heldout_v01_s8_method_diagnostic",
    "experiments.heldout_v01_soccer_inference",
    "experiments.real_data_validation",
    "experiments.stage10_audit_verified_count_claims",
    "experiments.stage10_soccer_second_dataset",
    "experiments.stage10_soccer_source_count_audit",
]

@pytest.mark.parametrize("module_name", MODULES)
def test_bundled_experiment_import(module_name):
    assert importlib.import_module(module_name)
