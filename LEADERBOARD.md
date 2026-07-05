# LLM Benchmark Leaderboard

> Last updated: 2026-07-05T05:57:16.447827+00:00

| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |
|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|
| 1 | gpt2 | 40.00% | 4/10 | 1.671s | 29.1 | 133 | cpu | OK |
| 2 | distilgpt2 | 20.00% | 2/10 | 1.179s | 41.2 | 163 | cpu | OK |

## Metric Definitions

| Metric | Description |
|--------|-------------|
| Reasoning Score | Fraction of 10 tasks answered correctly |
| Latency | Average time to generate up to 50 tokens |
| Throughput | Tokens generated per second |
| Memory | RSS increase (MB) after model load |

*Generated automatically by GitHub Actions.*
