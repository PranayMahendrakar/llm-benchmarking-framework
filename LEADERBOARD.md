# LLM Benchmark Leaderboard

> Last updated: 2026-03-29T04:31:42.623966+00:00

| Rank | Model | Reasoning Score | Correct | Latency (mean) | Throughput (tok/s) | Memory (MB) | Device | Status |
|------|-------|----------------|---------|---------------|-------------------|-------------|--------|--------|
| 1 | gpt2 | 40.00% | 4/10 | 1.657s | 29.8 | 138 | cpu | OK |
| 2 | distilgpt2 | 20.00% | 2/10 | 1.191s | 41.3 | 155 | cpu | OK |

## Metric Definitions

| Metric | Description |
|--------|-------------|
| Reasoning Score | Fraction of 10 tasks answered correctly |
| Latency | Average time to generate up to 50 tokens |
| Throughput | Tokens generated per second |
| Memory | RSS increase (MB) after model load |

*Generated automatically by GitHub Actions.*
