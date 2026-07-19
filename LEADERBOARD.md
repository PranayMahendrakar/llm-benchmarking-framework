# LLM Benchmark Leaderboard

> Last updated: 2026-07-19T05:13:37.559136+00:00

| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |
|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|
| 1 | gpt2 | 40.00% | 4/10 | 1.716s | 28.0 | 136 | cpu | OK |
| 2 | distilgpt2 | 20.00% | 2/10 | 1.236s | 39.9 | 154 | cpu | OK |

## Metric Definitions

| Metric | Description |
|--------|-------------|
| Reasoning Score | Fraction of 10 tasks answered correctly |
| Latency | Average time to generate up to 50 tokens |
| Throughput | Tokens generated per second |
| Memory | RSS increase (MB) after model load |

*Generated automatically by GitHub Actions.*
