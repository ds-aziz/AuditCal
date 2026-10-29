"""Independent reproduction of three frozen Soccer sample counts.

Read-only specifications derived from source scripts inspected strictly as text.
No AI-authored program is executed and no regression evidence is inferred.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOCCER_SHA = "6dbc24e6f62862b0fc083ef5dc70487cf51739032bd0a04b4fed8aab3a81889a"
CLAIMS_PATH = ROOT / "evaluation/heldout_v01_selected_claims.json"


def recalculate_soccer_samples(path: Path) -> dict:
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != SOCCER_SHA:
        raise ValueError("Public Soccer educational-copy SHA256 mismatch")
    df = pd.read_csv(path, low_memory=False)
    if len(df) != 146028:
        raise ValueError("Unexpected source row count")
    fields = ["rater1", "rater2", "height", "weight", "position",
              "birthday", "meanIAT", "meanExp", "leagueCountry",
              "games", "redCards", "playerShort", "refNum"]
    if any(k not in df.columns for k in fields):
        raise ValueError("Unexpected source columns")

    # S3 strict two-rater mean; parsed age and complete-case covariates.
    strict_mean = (df["rater1"] + df["rater2"]) / 2.0
    age_year = pd.to_datetime(df["birthday"], format="%d.%m.%Y", errors="coerce").dt.year
    s3_mask = (strict_mean.notna() & age_year.notna()
        & df[["height", "weight", "position", "meanIAT", "meanExp"]].notna().all(axis=1))
    s3_count = int(s3_mask.sum())

    # S7 skips missing individual rating by default in row-wise mean.
    permissive_mean = df[["rater1", "rater2"]].mean(axis=1, skipna=True)
    contrasting = (permissive_mean <= 0.25) | (permissive_mean >= 0.75)
    s7_mask = contrasting & df[["height", "weight"]].notna().all(axis=1)
    s7_count = int(s7_mask.sum())
    s7_leagues = int(df.loc[s7_mask, "leagueCountry"].nunique(dropna=True))

    # S8 uses same row-wise average, but complete model-case filtering.
    needed_s8 = ["position", "leagueCountry", "height", "weight",
                 "games", "redCards", "playerShort", "refNum"]
    s8_mask = contrasting & df[needed_s8].notna().all(axis=1)
    s8_count = int(s8_mask.sum())
    one_rating = df[["rater1", "rater2"]].notna().sum(axis=1).eq(1)
    stats = {
      "S3": {"analysis_dyads":s3_count,
             "rating_rule":"Both ratings needed; arithmetic NaNs propagate",
             "age_required":True,"meanIAT_meanExp_required":True},
      "S7": {"analysis_dyads":s7_count,"leagues":s7_leagues,
             "rating_rule":"One rating can survive row-wise mean skipna",
             "one_rater_rows_retained":int((s7_mask & one_rating).sum())},
      "S8": {"analysis_dyads":s8_count,
             "rating_rule":"Row-wise mean skipna; model variable complete-cases",
             "one_rater_rows_retained":int((s8_mask & one_rating).sum())}
    }
    selected = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    by_id = {x["claim_id"]:x for x in selected["claims"]}
    numbers = {
      "S3-C1": (s3_count, "Strict two-rater, age and complete-case filtered sample"),
      "S7-C1": (s7_count, "High/low rating and height/weight filtered sample"),
      "S7-C2": (s7_leagues, "Distinct leagueCountry within S7 filtered sample"),
      "S8-C1": (s8_count, "High/low rating and all model variables complete")
    }
    checks = []
    for cid, (value, context) in numbers.items():
        claim = by_id[cid]
        if claim["claim_type"] not in ("sample_size", "distinct_count"):
            raise ValueError(f"Frozen claim {cid} is not a sample/count claim")
        checks.append({
          "claim_id":cid, "reported":claim["reported"],
          "independently_recomputed":value,"sample_identity":context,
          "preliminary_numeric_agreement":int(claim["reported"])==value,
          "gold_label":None,
          "independent_second_human_reviewer":False,
          "note":"Not an independently adjudicated gold label"
        })
    return {
      "source_sha256":digest,"upstream_agent_code_executed":False,
      "upstream_code_hash_verified":True,
      "status":"SINGLE_RESEARCHER_RECONSTRUCTION_NOT_GOLD",
      "model_specific_samples":stats,"comparisons":checks,
      "checked":len(checks),
      "agreements":sum(c["preliminary_numeric_agreement"] for c in checks),
      "provenance_limit":"Pinned university educational CSV; OSF original byte matching pending"
    }


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--soccer", type=Path, required=True)
    p.add_argument("--output", type=Path,
                   default=Path("results/heldout_v01/filtered_soccer_sample_evidence.json"))
    args=p.parse_args()
    output=recalculate_soccer_samples(args.soccer)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print("FROZEN_FILTERED_SOCCER_READOUT",json.dumps(output),flush=True)
    # A numerical discrepancy is a finding, not an infrastructure failure.


if __name__=="__main__":
    main()
