# LLM Benchmarking Framework

> Automated evaluation of open-source LLMs — no API keys required.
> GitHub Actions runs benchmarks and updates the leaderboard on every push.

[![Benchmark & Leaderboard Update](https://github.com/PranayMahendrakar/llm-benchmarking-framework/actions/workflows/benchmark.yml/badge.svg)](https://github.com/PranayMahendrakar/llm-benchmarking-framework/actions/workflows/benchmark.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

This framework benchmarks open-source language models using **HuggingFace Transformers** for local inference — zero proprietary API keys needed.

| Feature | Details |
|---------|---------|
| Inference engine | HuggingFace `transformers` (CPU/GPU) |
| CI models | `distilgpt2`, `gpt2` (run automatically in GitHub Actions) |
| Local models | `microsoft/phi-2`, `mistralai/Mistral-7B-v0.1`, `meta-llama/Meta-Llama-3-8B` |
| Metrics | Reasoning score, latency, token throughput, memory usage |
| Leaderboard | Auto-updated JSON + Markdown on every run |

---

## Metrics Explained

| Metric | How it is measured |
|--------|--------------------|
| **Reasoning Score** | 10 keyword-match tasks across arithmetic, logic, common-sense & sequence domains |
| **Latency (mean / p50 / p90)** | Wall-clock time (seconds) to generate up to 50 tokens, averaged over 5 runs |
| **Token Throughput** | Tokens generated per second over 3 throughput runs |
| **Memory Footprint** | RSS increase (MB) measured before vs. after model load |

---

## Repository Structure

```
llm-benchmarking-framework/
├── .github/
│   └── workflows/
│       └── benchmark.yml        # CI: runs benchmarks + updates leaderboard
├── benchmarks/
│   └── run_benchmark.py         # Main benchmark script
├── scripts/
│   └── update_leaderboard.py    # Generates LEADERBOARD.md + results/leaderboard.json
├── configs/
│   └── models.json              # Model registry (CI-safe vs local-only)
├── results/
│   ├── benchmark_results.json   # Raw benchmark output (auto-generated)
│   └── leaderboard.json         # Ranked leaderboard (auto-generated)
├── LEADERBOARD.md               # Human-readable leaderboard (auto-generated)
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run CI-safe benchmarks (distilgpt2 + gpt2)

```bash
python benchmarks/run_benchmark.py --models distilgpt2 gpt2 --output results/benchmark_results.json
```

### 3. Update the leaderboard

```bash
python scripts/update_leaderboard.py
```

### 4. Run larger models locally

```bash
# Phi-2 (2.7B) — requires ~6GB RAM
python benchmarks/run_benchmark.py --models microsoft/phi-2 --max-new-tokens 100

# Mistral 7B via Ollama (install Ollama first)
# ollama pull mistral
# Then use: python benchmarks/run_benchmark.py --models mistralai/Mistral-7B-v0.1
```

---

## GitHub Actions

The workflow (`.github/workflows/benchmark.yml`) triggers on:

- **Every push** to `main` that touches benchmarks, scripts, or requirements
- **Weekly schedule** (Sundays at 02:00 UTC)
- **Manual dispatch** (choose any models and `max_new_tokens`)

After benchmarking, the action commits updated `results/` and `LEADERBOARD.md` back to the repo automatically.

---

## Model Tiers

| Tier | Models | Notes |
|------|--------|-------|
| `ci_safe` | `distilgpt2`, `gpt2` | Run in GitHub Actions (< 2GB RAM) |
| `ci_borderline` | `gpt2-medium` | May work in CI, not guaranteed |
| `local_only` | `phi-2`, Mistral-7B, LLaMA-3-8B | Run locally, push results |

---

## Contributing

1. Fork the repo
2. Add your model to `configs/models.json`
3. Run benchmarks locally and commit `results/benchmark_results.json`
4. Open a pull request

---

## License

MIT — see [LICENSE](LICENSE).
