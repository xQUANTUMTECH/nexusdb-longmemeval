# NexusDB on LongMemEval — every answer, every verdict

**85.6%** on [LongMemEval](https://github.com/xiaowu0162/LongMemEval)-S with GPT-4o as the answer model and the benchmark's official judge — level with or above every reproducible published memory system, with **no model calls to build memory**.

This repository holds the raw record of every run we made, including the weaker ones: answers in the benchmark's official format, judge outputs, and per-question traces (tokens, cost, latency, retrieval ranks). An interactive explorer of all 500 questions, with the passages handed to the model, is at **[xquantumtech.com/benchmark/longmemeval](https://xquantumtech.com/benchmark/longmemeval/)**.

*NexusDB is a memory layer for AI models by [X Quantum Tech](https://xquantumtech.com/it/nexusdb) (not the Delphi database). The engine is proprietary; this repository contains results, not engine code.*

## Headline (GPT-4o, official judge, original release)

| System | LongMemEval-S | Model calls to build memory |
|---|---|---|
| **NexusDB** | **85.6%** | none |
| EmergenceMem — internal (stated as not reproducible) | 86.0% | not stated |
| Mastra — Observational Memory | 84.2% | yes (observer and reflector models) |
| GPT-4o given only the right sessions ("oracle") | 82.4% | — |
| EmergenceMem — simple | 82.4% | not stated |
| Supermemory | 81.6% | not stated |
| Mastra — plain RAG baseline | 80.1% | none |
| Zep | 71.2% | yes (graph built with GPT-4o-mini) |

With GPT-4o-mini: **79.6%** vs Zep's **63.8%** on the same model, release and judge. Other systems' figures are as published by their makers; we did not reproduce them.

## Where we lose

1. Systems answering with newer models (e.g. Mastra 94.9% with gpt-5-mini, Hindsight 91.4% with Gemini 3 Pro) are not comparable: we have not run newer models.
2. A small open model alone (Gemma 3 4B: 56.8%) stays below Zep with GPT-4o-mini (63.8%): it finds the facts but cannot count across sessions or reason over dates.
3. On the ~10× larger M set we score 66.6% with GPT-4o-mini; no other system has published M results to compare with.

## Every run

All runs: 500 questions, official judge (gpt-4o-2024-08-06, official prompt, temperature 0). Nothing omitted.

| Answer model | Release | Setup | Overall | User detail | Assistant detail | Updates | Time | Multi-session | Preferences | Files |
|---|---|---|---|---|---|---|---|---|---|---|
| gpt-4o (OpenRouter) | original | v7 | **85.6%** | 97.1% | 100.0% | 93.6% | 85.7% | 74.4% | 60.0% | `gpt-4o_v7_orig` |
| gpt-4o-mini (OpenRouter) | original | v7 | **79.6%** | 97.1% | 100.0% | 83.3% | 76.7% | 68.4% | 53.3% | `gpt-4o-mini_v7_orig` |
| gpt-4o-mini (OpenRouter) | cleaned | v7 | **78.8%** | 97.1% | 100.0% | 82.0% | 78.2% | 66.2% | 46.7% | `gpt-4o-mini_v7` |
| gpt-4o-mini (OpenRouter) | cleaned | v4 | **77.6%** | 95.7% | 98.2% | 84.6% | 78.2% | 64.7% | 33.3% | `gpt-4o-mini_v4` |
| gpt-4o-mini (OpenRouter) | cleaned | v5 + full read path | **77.0%** | 95.7% | 100.0% | 84.6% | 75.9% | 63.9% | 33.3% | `gpt-4o-mini_v5_cmp` |
| gpt-4o-mini (OpenRouter) | cleaned | v2 | **76.8%** | 98.6% | 96.4% | 84.6% | 71.4% | 61.7% | 60.0% | `gpt-4o-mini_v2` |
| gpt-4o-mini (OpenRouter) | cleaned | v6 + full read path | **76.6%** | 97.1% | 100.0% | 84.6% | 74.4% | 63.9% | 30.0% | `gpt-4o-mini_v6_cmp` |
| gpt-4o-mini (OpenRouter) | original | v2 | **75.8%** | 98.6% | 98.2% | 82.0% | 71.4% | 60.2% | 53.3% | `gpt-4o-mini_v2_orig` |
| gpt-4o-mini (OpenRouter) | cleaned | v1 | **75.6%** | 98.6% | 98.2% | 84.6% | 69.9% | 61.7% | 43.3% | `gpt-4o-mini` |
| gpt-4o-mini (OpenRouter) | cleaned | v3 | **75.0%** | 97.1% | 98.2% | 83.3% | 69.2% | 59.4% | 53.3% | `gpt-4o-mini_v3` |
| gpt-4o-mini (OpenRouter) | original | v1 | **74.2%** | 98.6% | 98.2% | 84.6% | 67.7% | 59.4% | 40.0% | `gpt-4o-mini_orig` |
| gpt-4o-mini (OpenRouter) | cleaned | v4 + links appended | **72.2%** | 100.0% | 96.4% | 80.8% | 72.9% | 54.9% | 13.3% | `gpt-4o-mini_v4_full` |
| gpt-4o-mini (OpenRouter) | M | v2 | **66.6%** | 92.9% | 100.0% | 78.2% | 58.7% | 46.6% | 36.7% | `gpt-4o-mini_v2_M` |
| gemma-3-4b-it (open, local GPU) | cleaned | v2 | **56.8%** | 84.3% | 87.5% | 78.2% | 44.4% | 32.3% | 43.3% | `gemma-3-4b-it_v2` |
| gemma-3-4b-it (open, local GPU) | cleaned | v7 | **56.4%** | 80.0% | 85.7% | 78.2% | 47.4% | 33.1% | 33.3% | `gemma-3-4b-it_v7` |
| gemma-3-4b-it (open, local GPU) | cleaned | v1 | **52.2%** | 81.4% | 87.5% | 76.9% | 38.4% | 27.8% | 23.3% | `gemma-3-4b-it` |

Prompt versions: v1 base · v2 adds a personalisation rule · v3 adds dates computed in code · v4 adds step-by-step reasoning (only the final answer is judged) · v5–v6 add the full read path · v7 routes advice requests (detected from the question text) to a direct answer and every other question to step-by-step reasoning. v4–v6 did not show the computed dates in chat headers (script error, fixed in v7).

## Setup

- **Memory.** One cartridge per question, built only from that question's own history: each round is a user turn plus the assistant's reply, verbatim, stamped with the session date. No model calls to build memory.
- **Retrieval.** One search pass: hybrid search (dense + keyword) with reranking, top 10 passages handed to the model in time order. The right past session is among the 10 passages for 99.6% of questions. No agent, no tools.
- **Speed.** Building the memory from the whole history and searching it takes 0.96 s per question (median; 95th percentile 1.9 s) on a single L40S GPU, and 7.4 s on the ~10× larger M set (`sec` in `runs/ctx_*_trace.jsonl`). Times include the build; search alone over a ready cartridge was not timed separately.
- **Answer models.** GPT-4o and GPT-4o-mini via OpenRouter (temperature 0); Gemma 3 4B instruct on our own GPU (greedy decoding).
- **Judge.** The official `get_anscheck_prompt` from LongMemEval's `evaluate_qa.py`, gpt-4o-2024-08-06, temperature 0.
- **Releases.** `original` is the release used in Zep's published run; `cleaned` is the later cleaned release; `M` is the ~1.5M-token-per-question set. SHA-256 prefixes in `meta.json`.

## Files

| Path | Content |
|---|---|
| `meta.json` | Runs, per-type scores, datasets with hashes, answer prompts verbatim, retrieval and judge description |
| `runs/hyp_<run>.jsonl` | Answers in the benchmark's official hypothesis format |
| `runs/hyp_<run>.jsonl.eval-gpt-4o` | Official judge output per question |
| `runs/hyp_<run>_trace.jsonl` | Per-question trace: tokens, cost, latency, retries |
| `runs/ctx_*_trace.jsonl` | Retrieval traces: rank of the right session in dense, keyword, fused and reranked lists |
| `runs/official_evaluate_qa.py` | LongMemEval's official evaluation script, as used |
| `runs/lme_judge.py` | The wrapper we used to call the official judge prompt |

The passages handed to the model for each question (≈77 MB) are downloadable from the [results page](https://xquantumtech.com/benchmark/longmemeval/). Questions and histories are LongMemEval's and are not redistributed here: get them from the [official repository](https://github.com/xiaowu0162/LongMemEval).

## Re-scoring

```bash
# with the official LongMemEval repository checked out and an OpenAI key set
python runs/official_evaluate_qa.py gpt-4o runs/hyp_gpt-4o_v7_orig.jsonl path/to/longmemeval_s.json
```

## Scope

LongMemEval tests recall from short, synthetic chat histories (~115k tokens per question on the S set), answered in a single pass. It does not test procedures, tools, learning from verified use or memories at real working scale — the settings NexusDB is built for and covered by our other tests ([summary](https://github.com/xQUANTUMTECH/nexusdb-manifesto)).

## Contact

Maurizio Tarricone — Founder & CEO, X Quantum Tech FZE LLC · ceo@xquantumtech.com

© 2026 X Quantum Tech FZE LLC. Results may be cited with attribution.
