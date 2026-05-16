"""Publish a markdown scorecard from conformance and interop outputs."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    interop_path = Path("benchmarks/interop_report.json")
    interop = json.loads(interop_path.read_text()) if interop_path.exists() else {"summary": {"count": 0, "average_similarity": 0, "average_drift_delta": 1}}

    md = Path("benchmarks/interop_scorecard.md")
    lines = [
        "# ARIA Interop Scorecard",
        "",
        "## Latest Snapshot",
        f"- Cases: {interop['summary']['count']}",
        f"- Average Similarity: {interop['summary']['average_similarity']:.4f}",
        f"- Average Drift Delta: {interop['summary']['average_drift_delta']:.4f}",
        "",
        "## Interpretation",
        "- Higher average similarity is better.",
        "- Lower average drift delta is better.",
    ]
    md.write_text("\n".join(lines) + "\n")
    print(str(md))


if __name__ == "__main__":
    main()
