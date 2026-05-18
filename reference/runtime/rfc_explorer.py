"""RFC Explorer: build a machine-readable index of ARIA RFC documents."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

RFC_DIR = Path("docs/rfcs")

CATEGORY_RULES = [
    ("Protocol", ["Protocol_Stack", "Intent_Checksum"]),
    ("Runtime", ["Agent_Runtime", "Cognitive_Role", "Capability_Registry"]),
    ("Safety", ["Guardrails", "Budget", "Circuit_Breaker", "Canary", "Quorum"]),
    ("Interop", ["Interop", "Lineage", "Replay"]),
]


def _category_from_name(name: str) -> str:
    for cat, kws in CATEGORY_RULES:
        if any(k in name for k in kws):
            return cat
    return "General"


def _extract_status(text: str) -> str:
    m = re.search(r"Status:\s*([A-Za-z0-9_. -]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def _extract_depends(text: str) -> List[str]:
    m = re.search(r"Depends:\s*([^\n]+)", text)
    if not m:
        return []
    return [x.strip() for x in m.group(1).split(",") if x.strip()]


def build_rfc_index() -> Dict:
    rfcs: List[Dict] = []
    for p in sorted(RFC_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        title = lines[1].lstrip("# ") if len(lines) > 1 and lines[1].startswith("##") else p.stem
        rfc_id = p.stem.split("_")[0]
        rfcs.append(
            {
                "id": rfc_id,
                "title": title,
                "status": _extract_status(text),
                "path": str(p).replace("\\", "/"),
                "category": _category_from_name(p.stem),
                "depends_on": _extract_depends(text),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(RFC_DIR),
        "rfcs": rfcs,
    }


def save_index(path: str = "registry/rfc_index.json") -> str:
    obj = build_rfc_index()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    return str(out)


if __name__ == "__main__":
    print(save_index())
