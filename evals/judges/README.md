# Agent-Native Judge Layer

This directory documents the agent-native judging workflow for the Writing Harness.

No external API is required.

Instead of calling a hosted judging service, this workflow packages comparison tasks as judge packets that can be run by the same kind of agent surface that uses the Writing Harness skill.

## Why This Design

For a skill-first project, the evaluation UX should match the usage UX.

That means:

- benchmark tasks should be runnable by an agent using the skill
- comparisons should also be runnable by an agent using the skill
- deterministic scoring should remain available as the hard regression floor

## What the Judge Layer Does

It supports:

- pairwise comparison of two candidate runs
- structured JSON outputs
- trace-aware process QA
- cognitive-artifact QA
- machine-readable summaries
- aggregation across all benchmark cases

## Files

```text
evals/judges/
└── README.md
```

```text
scripts/
├── check_agent_native_run_status.py
├── prepare_agent_native_benchmark_run.py
├── prepare_agent_native_judge_run.py
├── prepare_agent_native_session.py
└── summarize_agent_native_judgments.py
```

## Workflow

### 1. Prepare candidate packets

```bash
python3 scripts/prepare_agent_native_session.py benchmark --outdir runs/prompt-a
```

This creates the benchmark packets plus a single-session runbook.

### 2. Ask an agent to complete the packets

Ask the agent to follow `runs/prompt-a/RUNBOOK.md` in one session.

### 3. Deterministically score the run

```bash
python3 scripts/run_writing_harness_benchmarks.py --candidate-dir runs/prompt-a/results
```

### 4. Prepare judge packets for pairwise comparison

```bash
python3 scripts/prepare_agent_native_session.py judge \
  --left-dir runs/prompt-a/results \
  --right-dir runs/prompt-b/results \
  --outdir runs/judge-a-vs-b
```

### 5. Ask an agent to complete the judge packets

Ask the agent to follow `runs/judge-a-vs-b/RUNBOOK.md` in one session.

### 6. Aggregate the judgments

```bash
python3 scripts/summarize_agent_native_judgments.py \
  --results-dir runs/judge-a-vs-b/results \
  --json evals/reports/judge-a-vs-b.json
```

## Expected Judge Output

Each case should return JSON with:

- `winner`
- `left_score`
- `right_score`
- `confidence`
- `summary`
- `strengths_left`
- `strengths_right`
- `risks_left`
- `risks_right`
- `trace_winner`
- `trace_notes_left`
- `trace_notes_right`
- `cognitive_winner`
- `cognitive_notes_left`
- `cognitive_notes_right`

This lets the judge layer stay structured and automatable without depending on an external API, while still checking whether the writing came from a disciplined harness process rather than a lucky one-shot.
