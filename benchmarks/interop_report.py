"""Generate interop benchmark report JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reference.interop.benchmark import evaluate_roundtrip_suite


def main() -> None:
    report = evaluate_roundtrip_suite("fixtures/interop/legacy_roundtrip_cases.json")
    out = Path("benchmarks/interop_report.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(str(out))


if __name__ == "__main__":
    main()
