# LLM Benchmark Leaderboard

> Last updated: 2026-11-01T08:25:41.589858+00:00

| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |
|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|
| 1 | gpt2 | 40.00% | 4/10 | 1.667s | 29.3 | 136 | cpu | OK |
| 2 | distilgpt2 | 20.00% | 2/10 | 1.212s | 41.0 | 157 | cpu | OK |

## Metric Definitions

| Metric | Description |
|--------|-------------|
| Reasoning Score | Fraction of 10 tasks answered correctly |
| Latency | Average time to generate up to 50 tokens |
| Throughput | Tokens generated per second |
| Memory | RSS increase (MB) after model load |

*Generated automatically by GitHub Actions.*
