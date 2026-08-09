# LLM Benchmark Leaderboard

> Last updated: 2026-08-09T03:25:59.459006+00:00

| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |
|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|
| 1 | gpt2 | 40.00% | 4/10 | 1.637s | 30.1 | 131 | cpu | OK |
| 2 | distilgpt2 | 20.00% | 2/10 | 1.175s | 42.0 | 154 | cpu | OK |

## Metric Definitions

| Metric | Description |
|--------|-------------|
| Reasoning Score | Fraction of 10 tasks answered correctly |
| Latency | Average time to generate up to 50 tokens |
| Throughput | Tokens generated per second |
| Memory | RSS increase (MB) after model load |

*Generated automatically by GitHub Actions.*
