"""Structural test for imports of ALL bundled independent research scripts.

Importing modules does not download source data or execute AI-authored research code.
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
    "experiments.heldout_v01_source_integrity",
    "experiments.heldout_v01_static_soccer_filters",
    "experiments.independent_metr_reanalysis",
    "experiments.ingest_published_agent_reports",
    "experiments.real_data_validation",
    "experiments.stage10_audit_verified_count_claims",
    "experiments.stage10_soccer_second_dataset",
    "experiments.stage10_soccer_source_count_audit",
    "experiments.stage10_soccer_source_triage",
    "experiments.stage11_audit_soccer_claims",
    "experiments.stage11_independent_soccer_models",
    "experiments.stage8_independent_method_variants",
    "experiments.stage8_multiagent_compare",
    "experiments.stage8_spec_inspection",
    "experiments.stage9_crossmodel_metr_reanalysis",
    "experiments.stage9_other_models_inventory",
    "experiments.verify_osf_soccer_original",
    "experiments.verify_public_agent_report"
]

@pytest.mark.parametrize("module_name", MODULES)
def test_bundled_experiment_import(module_name):
    assert importlib.import_module(module_name)
