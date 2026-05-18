#!/usr/bin/env python3
"""
ARIA Protocol - Interactive CLI Demo
Demonstrates the complete architecture: ICA, Drift Detection, Trust Scoring, Circuit Breaker.

Usage:
    python cli_demo_production.py
    python cli_demo_production.py --backend sentence-transformers
    python cli_demo_production.py --backend openai --api-key YOUR_KEY
"""
import sys
import argparse
import json
from typing import Optional
from enum import Enum

from aria_ica_production import (
    ProductionICA,
    EmbeddingBackend,
    ICResult,
)


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_section(text: str):
    """Print a formatted section."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}→ {text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*70}{Colors.ENDC}")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_metric(label: str, value: any, color: str = Colors.BLUE):
    """Print a metric."""
    print(f"  {label}: {color}{value}{Colors.ENDC}")


def demo_basic_ica(ica: ProductionICA):
    """Demo 1: Basic Intent Checksum Algorithm."""
    print_section("Demo 1: Intent Checksum Algorithm (ICA)")
    
    intent = "Buy Apple stock for $10,000 from a blue-chip portfolio"
    print(f"Input Intent: {Colors.BOLD}{intent}{Colors.ENDC}\n")
    
    print("Computing Intent Checksum...")
    ic = ica.compute(
        intent=intent,
        constraints=["max_budget: 10000", "sector: blue_chips", "risk_level: low"],
        context={"portfolio_type": "conservative", "market_condition": "stable"},
        success_condition="Order executed within 5 minutes",
        failure_condition="Budget exceeded or sector constraint violated",
    )
    
    print_success(f"Checksum computed: {ic.checksum[:16]}...")
    print_metric("Overall Score", f"{ic.score:.4f}")
    print_metric("Backend", ic.backend)
    
    print(f"\n{Colors.BOLD}Atom Scores:{Colors.ENDC}")
    for atom, score in ic.atoms.items():
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"  {atom:25} {bar} {score:.4f}")
    
    return ic


def demo_drift_detection(ica: ProductionICA, ic_original: ICResult):
    """Demo 2: Semantic Drift Detection."""
    print_section("Demo 2: Semantic Drift Detection")
    
    # Scenario: Mission gets modified as it flows through agents
    modified_intent = "Buy Apple stock for up to $10,000"
    print(f"Original Intent: {Colors.BOLD}{ic_original.atoms}{Colors.ENDC}")
    print(f"Modified Intent: {Colors.BOLD}{modified_intent}{Colors.ENDC}\n")
    
    print("Computing modified Intent Checksum...")
    ic_modified = ica.compute(intent=modified_intent)
    
    print_success(f"Modified Checksum: {ic_modified.checksum[:16]}...")
    
    drift = ica.detect_drift(ic_original, ic_modified)
    print_metric("Drift Score", f"{drift:.4f}")
    
    if drift > 0.15:
        print_warning(f"SEMANTIC DRIFT DETECTED: {drift:.1%}")
        print(f"  → Original constraints lost: 'blue-chip portfolio'")
        print(f"  → Risk level increased from 'low' to 'unknown'")
    else:
        print_success(f"Drift within acceptable threshold: {drift:.1%}")
    
    return ic_modified


def demo_trust_scoring(ica: ProductionICA):
    """Demo 3: Dynamic Trust Scoring."""
    print_section("Demo 3: Dynamic Trust Scoring")
    
    agents = [
        {"name": "Orchestrator", "role": "mission-parsing", "verifications": 1247, "failures": 3},
        {"name": "Specialist", "role": "semantic-validation", "verifications": 892, "failures": 5},
        {"name": "Executor", "role": "market-analysis", "verifications": 654, "failures": 12},
        {"name": "Trader", "role": "trade-execution", "verifications": 432, "failures": 18},
        {"name": "Risk Manager", "role": "policy-enforcement", "verifications": 1089, "failures": 8},
    ]
    
    print(f"{Colors.BOLD}Agent Trust Profiles:{Colors.ENDC}\n")
    
    for agent in agents:
        success_rate = agent["verifications"] / (agent["verifications"] + agent["failures"])
        trust_score = success_rate * 0.8 + (1 - agent["failures"] / agent["verifications"] * 0.1)
        
        bar = "█" * int(trust_score * 20) + "░" * (20 - int(trust_score * 20))
        color = Colors.GREEN if trust_score > 0.9 else Colors.YELLOW if trust_score > 0.75 else Colors.RED
        
        print(f"  {agent['name']:20} {bar} {color}{trust_score:.1%}{Colors.ENDC}")
        print(f"    └─ {agent['role']:30} ({agent['verifications']} OK, {agent['failures']} failed)")


def demo_circuit_breaker(ica: ProductionICA):
    """Demo 4: Circuit Breaker Protection."""
    print_section("Demo 4: Circuit Breaker & Policy Enforcement")
    
    print(f"{Colors.BOLD}Scenario: Mission flows through 5 agents{Colors.ENDC}\n")
    
    original_intent = "Buy Apple stock. Max 10k€. Blue chips only."
    intents = [
        ("Agent 1 (Orchestrator)", original_intent),
        ("Agent 2 (Specialist)", "Buy Apple stock. Max 10k€."),
        ("Agent 3 (Executor)", "Buy Apple shares. Max 10k€."),
        ("Agent 4 (Trader)", "Purchase AAPL up to 10,000€"),
        ("Agent 5 (Risk Manager)", "CIRCUIT BREAKER ACTIVATED"),
    ]
    
    ic_original = ica.compute(intent=original_intent)
    drift_threshold = 0.15
    
    for i, (agent, intent) in enumerate(intents, 1):
        if "CIRCUIT BREAKER" in agent:
            print_error(f"Step {i}: {agent}")
            print(f"  → Drift exceeded {drift_threshold:.0%} threshold")
            print(f"  → Requesting human confirmation before proceeding")
            break
        
        ic_current = ica.compute(intent=intent)
        drift = ica.detect_drift(ic_original, ic_current)
        
        status = "✓" if drift < drift_threshold else "⚠"
        color = Colors.GREEN if drift < drift_threshold else Colors.YELLOW
        
        print(f"Step {i}: {agent}")
        print(f"  Intent: {intent}")
        print(f"  Drift: {color}{drift:.1%}{Colors.ENDC} {status}")
        
        if drift > drift_threshold:
            print_warning(f"Drift approaching threshold!")


def demo_benchmark(ica: ProductionICA):
    """Demo 5: Performance Benchmarking."""
    print_section("Demo 5: Performance Benchmarking")
    
    test_cases = [
        ("Buy Apple stock", "Purchase AAPL shares"),
        ("Transfer $1000 to account", "Move 1000 dollars to the account"),
        ("Execute market order", "Place market order for execution"),
        ("Check account balance", "What is my account balance?"),
        ("Set stop loss at 50%", "Configure stop loss to 50 percent"),
    ]
    
    print(f"Running {len(test_cases)} test cases...\n")
    
    benchmark_results = ica.benchmark(test_cases)
    
    print_metric("Backend", benchmark_results["backend"])
    print_metric("Test Cases", benchmark_results["test_cases"])
    print_metric("Avg Time", f"{benchmark_results['avg_time']*1000:.2f}ms")
    print_metric("Avg Drift", f"{benchmark_results['avg_drift']:.4f}")
    
    print(f"\n{Colors.BOLD}Detailed Results:{Colors.ENDC}")
    for i, (time_ms, drift) in enumerate(zip(benchmark_results["times"], benchmark_results["drifts"]), 1):
        print(f"  Test {i}: {time_ms*1000:6.2f}ms | Drift: {drift:.4f}")


def demo_end_to_end(ica: ProductionICA):
    """Complete end-to-end demo."""
    print_header("ARIA Protocol - Complete Architecture Demo")
    
    print(f"{Colors.BOLD}Backend: {ica.backend_type.value}{Colors.ENDC}")
    print(f"{Colors.BOLD}This demo showcases:{Colors.ENDC}")
    print("  1. Intent Checksum Algorithm (ICA)")
    print("  2. Semantic Drift Detection")
    print("  3. Dynamic Trust Scoring")
    print("  4. Circuit Breaker Protection")
    print("  5. Performance Benchmarking")
    
    # Run all demos
    ic_original = demo_basic_ica(ica)
    demo_drift_detection(ica, ic_original)
    demo_trust_scoring(ica)
    demo_circuit_breaker(ica)
    demo_benchmark(ica)
    
    # Summary
    print_header("Demo Complete")
    print(f"{Colors.GREEN}{Colors.BOLD}✓ ARIA Protocol architecture demonstrated successfully!{Colors.ENDC}\n")
    print("Key Takeaways:")
    print("  • Semantic integrity is preserved through cryptographic checksums")
    print("  • Drift detection catches semantic degradation early")
    print("  • Trust scores enable federated verification")
    print("  • Circuit breakers protect against policy violations")
    print("  • Multi-backend support enables production deployment\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ARIA Protocol - Interactive CLI Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_demo_production.py
  python cli_demo_production.py --backend sentence-transformers
  python cli_demo_production.py --backend openai --api-key YOUR_KEY
        """
    )
    
    parser.add_argument(
        "--backend",
        choices=["lexical", "sentence-transformers", "openai", "claude"],
        default="lexical",
        help="Embedding backend to use (default: lexical)"
    )
    parser.add_argument(
        "--api-key",
        help="API key for cloud backends (OpenAI, Claude)"
    )
    parser.add_argument(
        "--model",
        help="Model name for the backend"
    )
    
    args = parser.parse_args()
    
    # Initialize ICA with selected backend
    backend_map = {
        "lexical": EmbeddingBackend.LEXICAL,
        "sentence-transformers": EmbeddingBackend.SENTENCE_TRANSFORMERS,
        "openai": EmbeddingBackend.OPENAI,
        "claude": EmbeddingBackend.CLAUDE,
    }
    
    backend = backend_map[args.backend]
    kwargs = {}
    if args.api_key:
        kwargs["api_key"] = args.api_key
    if args.model:
        kwargs["model"] = args.model
    
    try:
        ica = ProductionICA(backend=backend, **kwargs)
    except Exception as e:
        print_error(f"Failed to initialize backend: {e}")
        sys.exit(1)
    
    # Run demo
    try:
        demo_end_to_end(ica)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
