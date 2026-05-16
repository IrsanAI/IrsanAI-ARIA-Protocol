"""Minimal ARIA CLI: validate | ack | ica | calibrate | interop-benchmark | hop-demo | rrc."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reference.runtime.execution_specialist import ExecutionSpecialist
from reference.runtime.aria_ica import semantic_similarity
from reference.runtime.calibration import evaluate_tier_matrix
from reference.runtime.rrc import emit_rrc_capsule
from reference.runtime.validation import validate_aria_packet, validate_rrc_capsule, validate_semantic_ack
from reference.interop.benchmark import evaluate_roundtrip_suite
from reference.runtime.hop_chain import run_hop_chain
from reference.runtime.guardrails import guardrail_decision
from reference.runtime.lineage import build_intent_lineage_graph
from reference.runtime.budget import budget_for_tier, update_budget
from reference.interop.benchmark_v2 import compare_profiles
from reference.runtime.canary import run_canary_suite
from reference.runtime.circuit_breaker import circuit_threshold_for_tier, next_circuit_state
from reference.runtime.quorum import quorum_for_tier, evaluate_quorum
from reference.runtime.meta_cognitive_router import build_role_map


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


def cmd_calibrate(args):
    report = evaluate_tier_matrix(args.matrix)
    print(json.dumps(report))


def cmd_interop_benchmark(args):
    report = evaluate_roundtrip_suite(args.fixtures)
    print(json.dumps(report))


def cmd_hop_demo(args):
    source = _load_json(args.source)
    report = run_hop_chain(
        source_atoms=source,
        hops=args.hops,
        profile=args.profile,
        mission_fingerprint=args.mission_fingerprint,
        tier=args.tier,
    )
    print(json.dumps(report))


def cmd_guardrail(args):
    d = guardrail_decision(
        similarity=args.similarity,
        profile=args.profile,
        tier=args.tier,
        chain_depth=args.chain_depth,
        moving_drift=args.moving_drift,
    )
    print(json.dumps(d))


def cmd_chain(args):
    source = _load_json(args.source)
    report = run_hop_chain(
        source_atoms=source,
        hops=args.hops,
        profile=args.profile,
        mission_fingerprint=args.mission_fingerprint,
        tier=args.tier,
    )
    print(json.dumps(report))


def cmd_lineage(args):
    hops = _load_json(args.hops)
    graph = build_intent_lineage_graph(args.mission_fingerprint, hops, args.profile)
    print(json.dumps(graph))


def cmd_interop_compare(args):
    report = compare_profiles(args.fixtures)
    print(json.dumps(report))


def cmd_budget(args):
    bmax = args.budget_max if args.budget_max is not None else budget_for_tier(args.tier)
    report = update_budget(budget_max=bmax, budget_used=args.budget_used, drift_delta=args.drift_delta)
    print(json.dumps(report))


def cmd_canary(args):
    report = run_canary_suite(args.suite)
    print(json.dumps(report))


def cmd_circuit(args):
    threshold = args.threshold if args.threshold is not None else circuit_threshold_for_tier(args.tier)
    out = next_circuit_state(
        current_state=args.state,
        event_count=args.event_count,
        threshold=threshold,
        cooldown_remaining=args.cooldown_remaining,
        risk_event=args.risk_event,
    )
    print(json.dumps(out))


def cmd_quorum(args):
    votes = _load_json(args.votes)
    q = args.quorum_ratio if args.quorum_ratio is not None else quorum_for_tier(args.tier)
    report = evaluate_quorum(votes=votes, quorum_ratio=q)
    print(json.dumps(report))


def cmd_rolemap(args):
    role_map = build_role_map(task_id=args.task_id, task_text=args.task_text, activation_threshold=args.threshold)
    print(json.dumps(role_map))


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

    pc = sp.add_parser("calibrate")
    pc.add_argument("--matrix", required=True, help="JSON tier matrix path")
    pc.set_defaults(func=cmd_calibrate)

    pb = sp.add_parser("interop-benchmark")
    pb.add_argument("--fixtures", required=True, help="JSON fixtures for legacy roundtrip")
    pb.set_defaults(func=cmd_interop_benchmark)


    pg = sp.add_parser("guardrail")
    pg.add_argument("--similarity", required=True, type=float)
    pg.add_argument("--profile", default="strict", choices=["strict", "balanced", "exploratory"])
    pg.add_argument("--tier", default="finance")
    pg.add_argument("--chain-depth", type=int, default=1)
    pg.add_argument("--moving-drift", type=float, default=0.0)
    pg.set_defaults(func=cmd_guardrail)

    ph = sp.add_parser("hop-demo")
    ph.add_argument("--source", required=True, help="JSON file with 5 source atoms")
    ph.add_argument("--hops", type=int, default=4)
    ph.add_argument("--profile", default="strict", choices=["strict", "balanced", "exploratory"])
    ph.add_argument("--mission-fingerprint", default="mf-hop-chain")
    ph.add_argument("--tier", default="finance")
    ph.set_defaults(func=cmd_hop_demo)

    pcn = sp.add_parser("chain")
    pcn.add_argument("--source", required=True, help="JSON file with 5 source atoms")
    pcn.add_argument("--hops", type=int, default=4)
    pcn.add_argument("--profile", default="strict", choices=["strict", "balanced", "exploratory"])
    pcn.add_argument("--tier", default="finance")
    pcn.add_argument("--mission-fingerprint", default="mf-chain")
    pcn.set_defaults(func=cmd_chain)

    px = sp.add_parser("interop-compare")
    px.add_argument("--fixtures", required=True, help="lossy roundtrip fixtures")
    px.set_defaults(func=cmd_interop_compare)

    pl = sp.add_parser("lineage")
    pl.add_argument("--mission-fingerprint", required=True)
    pl.add_argument("--hops", required=True, help="JSON file containing hop list")
    pl.add_argument("--profile", default="strict", choices=["strict", "balanced", "exploratory"])
    pl.set_defaults(func=cmd_lineage)

    prm = sp.add_parser("rolemap")
    prm.add_argument("--task-id", required=True)
    prm.add_argument("--task-text", required=True)
    prm.add_argument("--threshold", type=float, default=0.3)
    prm.set_defaults(func=cmd_rolemap)

    pq = sp.add_parser("quorum")
    pq.add_argument("--tier", default="finance")
    pq.add_argument("--votes", required=True, help="JSON file with vote list")
    pq.add_argument("--quorum-ratio", type=float)
    pq.set_defaults(func=cmd_quorum)

    pcb = sp.add_parser("circuit")
    pcb.add_argument("--tier", default="finance")
    pcb.add_argument("--state", default="closed", choices=["closed", "open", "half_open"])
    pcb.add_argument("--event-count", type=int, default=0)
    pcb.add_argument("--threshold", type=int)
    pcb.add_argument("--cooldown-remaining", type=int, default=0)
    pcb.add_argument("--risk-event", action="store_true")
    pcb.set_defaults(func=cmd_circuit)

    pcy = sp.add_parser("canary")
    pcy.add_argument("--suite", required=True, help="canary suite JSON")
    pcy.set_defaults(func=cmd_canary)

    pbg = sp.add_parser("budget")
    pbg.add_argument("--tier", default="finance")
    pbg.add_argument("--budget-max", type=float)
    pbg.add_argument("--budget-used", type=float, default=0.0)
    pbg.add_argument("--drift-delta", type=float, required=True)
    pbg.set_defaults(func=cmd_budget)

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
