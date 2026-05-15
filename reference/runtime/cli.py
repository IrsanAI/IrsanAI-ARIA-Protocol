"""Minimal ARIA CLI: validate | ack | rrc."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reference.runtime.execution_specialist import ExecutionSpecialist
from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.rrc import emit_rrc_capsule
from reference.runtime.validation import validate_aria_packet, validate_rrc_capsule, validate_semantic_ack


def _load_json(path: str):
    return json.loads(Path(path).read_text())


def cmd_validate(args):
    data = _load_json(args.input)
    if args.kind == "packet":
        validate_aria_packet(data)
    elif args.kind == "ack":
        validate_semantic_ack(data)
    elif args.kind == "rrc":
        validate_rrc_capsule(data)
    print("valid")


def cmd_ack(args):
    specialist = ExecutionSpecialist()
    result = specialist.semantic_ack(args.received, args.recomputed, profile=args.profile)
    print(json.dumps({"status": result.status, "delta": result.delta, "profile": args.profile}))


def cmd_rrc(args):
    hops = _load_json(args.hops)
    events = _load_json(args.events) if args.events else []
    capsule = emit_rrc_capsule(
        capsule_id=args.capsule_id,
        mission_fingerprint=args.mission_fingerprint,
        hop_sequence=hops,
        final_outcome=args.final_outcome,
        audit_signature=args.audit_signature,
        accountability_events=events,
    )
    print(json.dumps(capsule))


def cmd_ica(args):
    source = _load_json(args.source)
    received = _load_json(args.received)
    sim = semantic_similarity(source, received)
    print(json.dumps({"semantic_similarity": sim}))


def main():
    p = argparse.ArgumentParser(prog="aria")
    sp = p.add_subparsers(dest="cmd", required=True)

    pv = sp.add_parser("validate")
    pv.add_argument("kind", choices=["packet", "ack", "rrc"])
    pv.add_argument("input")
    pv.set_defaults(func=cmd_validate)

    pa = sp.add_parser("ack")
    pa.add_argument("--received", required=True)
    pa.add_argument("--recomputed", required=True)
    pa.add_argument("--profile", default="balanced", choices=["strict", "balanced", "exploratory"])
    pa.set_defaults(func=cmd_ack)

    pi = sp.add_parser("ica")
    pi.add_argument("--source", required=True, help="JSON file with 5 source atoms")
    pi.add_argument("--received", required=True, help="JSON file with 5 received atoms")
    pi.set_defaults(func=cmd_ica)

    pr = sp.add_parser("rrc")
    pr.add_argument("--capsule-id", required=True)
    pr.add_argument("--mission-fingerprint", required=True)
    pr.add_argument("--hops", required=True, help="JSON file with hop sequence array")
    pr.add_argument("--final-outcome", required=True)
    pr.add_argument("--audit-signature", required=True)
    pr.add_argument("--events", help="optional JSON file with accountability events array")
    pr.set_defaults(func=cmd_rrc)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
