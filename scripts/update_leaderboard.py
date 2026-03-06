#!/usr/bin/env python3
"""
Leaderboard Updater - reads benchmark_results.json and updates leaderboard.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

RESULTS_FILE = Path("results/benchmark_results.json")
LEADERBOARD_JSON = Path("results/leaderboard.json")
LEADERBOARD_MD = Path("LEADERBOARD.md")


def load_results():
    if not RESULTS_FILE.exists():
        print(f"ERROR: {RESULTS_FILE} not found. Run benchmarks first.")
        sys.exit(1)
    with open(RESULTS_FILE) as fh:
        return json.load(fh)


def extract_row(result):
    if "error" in result:
        return {
            "model_id": result["model_id"],
            "timestamp": result.get("timestamp", "N/A"),
            "reasoning_score": None,
            "latency_mean_s": None,
            "throughput_tok_s": None,
            "memory_footprint_mb": None,
            "status": "FAILED",
        }
    reasoning = result.get("reasoning", {})
    latency = result.get("latency", {})
    throughput = result.get("throughput", {})
    memory = result.get("memory_mb", {})
    return {
        "model_id": result["model_id"],
        "timestamp": result.get("timestamp", "N/A"),
        "reasoning_score": reasoning.get("score", 0),
        "reasoning_correct": f"{reasoning.get('correct', 0)}/{reasoning.get('total', 0)}",
        "latency_mean_s": latency.get("mean_s", 0),
        "latency_p50_s": latency.get("p50_s", 0),
        "latency_p90_s": latency.get("p90_s", 0),
        "throughput_tok_s": throughput.get("tokens_per_second", 0),
        "memory_footprint_mb": memory.get("model_footprint", 0),
        "memory_peak_mb": memory.get("peak", 0),
        "device": result.get("device", "cpu"),
        "status": "OK",
    }


def rank_rows(rows):
    ok = [r for r in rows if r["status"] == "OK"]
    failed = [r for r in rows if r["status"] != "OK"]
    ok.sort(key=lambda r: (-(r["reasoning_score"] or 0), r["latency_mean_s"] or 0))
    for i, r in enumerate(ok, 1):
        r["rank"] = i
    for r in failed:
        r["rank"] = "N/A"
    return ok + failed


def build_markdown(rows, generated_at):
    header = [
        "# LLM Benchmark Leaderboard",
        "",
        f"> Last updated: {generated_at}",
        "",
        "| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |",
        "|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|",
    ]
    table = []
    for row in rows:
        rank = row.get("rank", "N/A")
        model = row["model_id"]
        if row["status"] == "OK":
            rs = f"{row['reasoning_score']:.2%}"
            correct = row.get("reasoning_correct", "N/A")
            lat = f"{row['latency_mean_s']:.3f}s"
            thr = f"{row['throughput_tok_s']:.1f}"
            mem = f"{row['memory_footprint_mb']:.0f}"
            dev = row.get("device", "cpu")
            status = "OK"
        else:
            rs = correct = lat = thr = mem = dev = "ERROR"
            status = "FAILED"
        table.append(f"| {rank} | {model} | {rs} | {correct} | {lat} | {thr} | {mem} | {dev} | {status} |")
    footer = [
        "",
        "## Metric Definitions",
        "",
        "| Metric | Description |",
        "|--------|-------------|",
        "| Reasoning Score | Fraction of 10 tasks answered correctly |",
        "| Latency | Average time to generate up to 50 tokens |",
        "| Throughput | Tokens generated per second |",
        "| Memory | RSS increase (MB) after model load |",
        "",
        "*Generated automatically by GitHub Actions.*",
    ]
    return "\n".join(header + table + footer) + "\n"


def main():
    results = load_results()
    rows = [extract_row(r) for r in results]
    rows = [r for r in rows if r is not None]
    ranked = rank_rows(rows)
    LEADERBOARD_JSON.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    leaderboard_data = {
        "generated_at": generated_at,
        "total_models": len(ranked),
        "leaderboard": ranked,
    }
    with open(LEADERBOARD_JSON, "w") as fh:
        json.dump(leaderboard_data, fh, indent=2)
    print(f"Saved JSON leaderboard to {LEADERBOARD_JSON}")
    md = build_markdown(ranked, generated_at)
    with open(LEADERBOARD_MD, "w") as fh:
        fh.write(md)
    print(f"Saved Markdown leaderboard to {LEADERBOARD_MD}")
    print("\nTop models:")
    for row in ranked[:5]:
        if row["status"] == "OK":
            print(f"  #{row['rank']} {row['model_id']} | reasoning: {row['reasoning_score']:.2%} | latency: {row['latency_mean_s']:.3f}s")


if __name__ == "__main__":
    main()
