"""CLI: python -m auditcal.cli examples/claims.jsonl"""
import argparse
import json
from pathlib import Path
from .core import audit

def main() -> None:
    parser = argparse.ArgumentParser(description="AuditCal structured-claim demo")
    parser.add_argument("input", type=Path, help="JSONL with one claim per line")
    args = parser.parse_args()
    with args.input.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("Expected JSON object")
                output = audit(value).to_dict()
            except (json.JSONDecodeError, ValueError) as error:
                output = {"line": index, "status": "UNVERIFIABLE", "reason": str(error)}
            print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
