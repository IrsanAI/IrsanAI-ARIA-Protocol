"""Generate profile comparison report (bridge-safe vs bridge-legacy)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reference.interop.benchmark_v2 import compare_profiles


def main() -> None:
    report = compare_profiles("fixtures/interop/legacy_roundtrip_lossy_cases.json")
    out = Path("benchmarks/interop_compare_report.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(str(out))


if __name__ == "__main__":
    main()
