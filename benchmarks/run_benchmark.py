#!/usr/bin/env python3
"""
LLM Benchmarking Framework
Evaluates open-source models on reasoning, latency, throughput, and memory usage.
Supports: DistilGPT2, GPT-2, Phi-2 (small variant), and other HuggingFace models.
"""

import json
import time
import argparse
import traceback
from pathlib import Path
from datetime import datetime, timezone

import psutil
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

REASONING_TASKS = [
    {"id": "arithmetic_1", "prompt": "Question: What is 15 + 27? Answer:", "expected_keywords": ["42"], "category": "arithmetic"},
    {"id": "logic_1", "prompt": "Question: If all cats are animals and all animals need food, do cats need food? Answer:", "expected_keywords": ["yes", "true", "do"], "category": "logic"},
    {"id": "common_sense_1", "prompt": "Question: What comes after Monday? Answer:", "expected_keywords": ["tuesday"], "category": "common_sense"},
    {"id": "arithmetic_2", "prompt": "Question: What is 100 divided by 4? Answer:", "expected_keywords": ["25"], "category": "arithmetic"},
    {"id": "logic_2", "prompt": "Question: Is the sky blue during the day? Answer:", "expected_keywords": ["yes", "true"], "category": "logic"},
    {"id": "common_sense_2", "prompt": "Question: How many days are in a week? Answer:", "expected_keywords": ["7", "seven"], "category": "common_sense"},
    {"id": "arithmetic_3", "prompt": "Question: What is 8 multiplied by 7? Answer:", "expected_keywords": ["56"], "category": "arithmetic"},
    {"id": "sequence_1", "prompt": "Question: What is the next number in the sequence: 2, 4, 6, 8? Answer:", "expected_keywords": ["10"], "category": "sequence"},
    {"id": "common_sense_3", "prompt": "Question: What season comes after winter? Answer:", "expected_keywords": ["spring"], "category": "common_sense"},
    {"id": "logic_3", "prompt": "Question: If a car has 4 wheels and a bike has 2 wheels, how many wheels do 2 cars and 1 bike have? Answer:", "expected_keywords": ["10"], "category": "logic"},
]

THROUGHPUT_PROMPT = (
    "The history of artificial intelligence began in antiquity with myths and stories "
    "of artificial beings endowed with intelligence or consciousness by master craftsmen."
)


def get_memory_mb():
    import psutil
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)


def score_response(response, keywords):
    lower = response.lower()
    return any(kw.lower() in lower for kw in keywords)


class ModelBenchmark:
    def __init__(self, model_id, device="cpu", max_new_tokens=50):
        self.model_id = model_id
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.tokenizer = None
        self.model = None

    def load(self):
        print(f"  Loading tokenizer for {self.model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        print(f"  Loading model for {self.model_id}...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True, trust_remote_code=True
        )
        self.model.to(self.device)
        self.model.eval()

    def generate(self, prompt):
        inputs = self.tokenizer(
            prompt, return_tensors="pt", padding=True, truncation=True, max_length=512
        ).to(self.device)
        input_len = inputs["input_ids"].shape[1]
        start = time.perf_counter()
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        elapsed = time.perf_counter() - start
        generated_ids = outputs[0][input_len:]
        tokens_generated = len(generated_ids)
        decoded = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return decoded, elapsed, tokens_generated

    def run_reasoning(self):
        correct = 0
        task_results = []
        for task in REASONING_TASKS:
            try:
                response, latency, _ = self.generate(task["prompt"])
                passed = score_response(response, task["expected_keywords"])
                if passed:
                    correct += 1
                task_results.append({
                    "id": task["id"], "category": task["category"],
                    "passed": passed, "latency_s": round(latency, 4),
                    "response_snippet": response[:80]
                })
            except Exception as exc:
                task_results.append({"id": task["id"], "category": task["category"], "passed": False, "error": str(exc)})
        return {"score": round(correct / len(REASONING_TASKS), 4), "correct": correct, "total": len(REASONING_TASKS), "tasks": task_results}

    def run_latency(self, runs=5):
        prompt = "Once upon a time in a land far away,"
        latencies = []
        for _ in range(runs):
            _, elapsed, _ = self.generate(prompt)
            latencies.append(elapsed)
        latencies.sort()
        return {
            "mean_s": round(sum(latencies) / len(latencies), 4),
            "p50_s": round(latencies[len(latencies) // 2], 4),
            "p90_s": round(latencies[int(len(latencies) * 0.9)], 4),
            "min_s": round(latencies[0], 4), "max_s": round(latencies[-1], 4)
        }

    def run_throughput(self):
        total_tokens = 0
        start = time.perf_counter()
        for _ in range(3):
            _, _, tokens = self.generate(THROUGHPUT_PROMPT)
            total_tokens += tokens
        elapsed = time.perf_counter() - start
        return {"tokens_per_second": round(total_tokens / elapsed, 2), "total_tokens": total_tokens, "elapsed_s": round(elapsed, 4)}

    def run_all(self):
        mem_before = get_memory_mb()
        self.load()
        mem_after_load = get_memory_mb()
        print("  Running reasoning tasks...")
        reasoning = self.run_reasoning()
        print("  Running latency benchmark...")
        latency = self.run_latency()
        print("  Running throughput benchmark...")
        throughput = self.run_throughput()
        mem_peak = get_memory_mb()
        return {
            "model_id": self.model_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "device": self.device,
            "reasoning": reasoning,
            "latency": latency,
            "throughput": throughput,
            "memory_mb": {
                "before_load": round(mem_before, 2),
                "after_load": round(mem_after_load, 2),
                "model_footprint": round(mem_after_load - mem_before, 2),
                "peak": round(mem_peak, 2)
            }
        }


def parse_args():
    parser = argparse.ArgumentParser(description="LLM Benchmark Runner")
    parser.add_argument("--models", nargs="+", default=["distilgpt2"], help="HuggingFace model IDs")
    parser.add_argument("--output", type=str, default="results/benchmark_results.json")
    parser.add_argument("--max-new-tokens", type=int, default=50)
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "cuda", "mps"])
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    all_results = []
    for model_id in args.models:
        print(f"\n{'='*60}\nBenchmarking: {model_id}\n{'='*60}")
        try:
            bench = ModelBenchmark(model_id=model_id, device=args.device, max_new_tokens=args.max_new_tokens)
            result = bench.run_all()
            all_results.append(result)
            print(f"  Done | Reasoning: {result['reasoning']['score']:.2%} | Latency: {result['latency']['mean_s']:.3f}s | Throughput: {result['throughput']['tokens_per_second']:.1f} tok/s")
        except Exception:
            print(f"  Failed to benchmark {model_id}:")
            traceback.print_exc()
            all_results.append({"model_id": model_id, "timestamp": datetime.now(timezone.utc).isoformat(), "error": traceback.format_exc()})
    with open(output_path, "w") as fh:
        json.dump(all_results, fh, indent=2)
    print(f"\nResults saved to {output_path}")
    return all_results


if __name__ == "__main__":
    main()
