# Writing Harness Benchmark Suite

This directory contains the end-to-end benchmark suite for the Writing Harness.

Unlike the lighter eval layer in `evals/README.md`, this suite tests actual rewrite tasks. It is designed to answer a harder question:

> Can this harness help produce materially better writing on realistic tasks?

## What This Suite Measures

Each benchmark case includes:

- an input draft
- a task brief
- audience and surface context
- required facts to preserve
- weak patterns to remove
- stronger signals to introduce
- a gold rewrite

The benchmark runner scores a candidate rewrite against those constraints.

## Benchmark Philosophy

This suite is intentionally harness-first.

It does not try to declare one universally correct rewrite. Instead, it checks whether the rewrite behaves like a good result from this harness:

- preserves the important facts
- removes obvious generic filler
- increases specificity
- shows stronger judgment
- respects the target audience and surface

That makes it suitable for:

- prompt regression testing
- comparing prompt variants
- comparing model backends
- validating a new skill revision
- checking whether the harness still steers toward authored quality

## Benchmark Layout

```text
evals/benchmarks/
├── README.md
├── cases.json
└── gold/
    ├── finance-landing-page.md
    ├── founder-update.md
    ├── internal-memo.md
    └── technical-explainer.md
```

## Running the Benchmark

### 1. Sanity check the suite

This compares the raw input drafts against the gold rewrites.

```bash
python3 scripts/run_writing_harness_benchmarks.py --sanity
```

Expected result:

- gold outputs should score much higher than the raw inputs
- the suite should fail if it cannot tell the difference

### 2. Evaluate the gold set directly

```bash
python3 scripts/run_writing_harness_benchmarks.py --use-gold
```

### 3. Evaluate candidate rewrites

Put one file per case in a directory:

```text
my-run/
├── finance-landing-page.md
├── founder-update.md
├── internal-memo.md
└── technical-explainer.md
```

Then run:

```bash
python3 scripts/run_writing_harness_benchmarks.py --candidate-dir my-run
```

### 4. Emit prompt packets for benchmark execution

If you want to run the benchmark with a model manually or through another tool:

```bash
python3 scripts/run_writing_harness_benchmarks.py --emit-prompts /tmp/writing-harness-prompts
```

This creates one prompt packet per case.

### 5. Prepare an agent-native candidate run

```bash
python3 scripts/prepare_agent_native_session.py benchmark --outdir runs/prompt-a
```

This creates:

- one packet per case in `runs/prompt-a/packets/`
- a manifest in `runs/prompt-a/run-manifest.json`
- a one-session runbook in `runs/prompt-a/RUNBOOK.md`

Then use your agent surface with the Writing Harness skill to complete the whole session from the runbook and write the final output into `runs/prompt-a/results/`.

You can check progress at any time:

```bash
python3 scripts/check_agent_native_run_status.py --manifest runs/prompt-a/run-manifest.json
```

### 6. Evaluate the candidate run

```bash
python3 scripts/run_writing_harness_benchmarks.py \
  --candidate-dir runs/prompt-a/results
```

### 7. Compare two runs with an agent-native judge

```bash
python3 scripts/prepare_agent_native_session.py judge \
  --left-dir runs/prompt-a/results \
  --right-dir runs/prompt-b/results \
  --outdir runs/judge-a-vs-b
```

This creates judge packets, a judge manifest, and a one-session judge runbook in `runs/judge-a-vs-b/RUNBOOK.md`.

Then use your agent surface to complete the whole judge session from the runbook and write JSON results into `runs/judge-a-vs-b/results/`.

Finally, aggregate the judgments:

```bash
python3 scripts/summarize_agent_native_judgments.py \
  --results-dir runs/judge-a-vs-b/results \
  --json evals/reports/judge-a-vs-b.json
```

## Scoring Model

Each case is scored on deterministic harness-aligned criteria:

- word-count fit
- fact preservation
- required strengthening signals
- banned phrase removal
- reduction of known weak patterns
- presence of judgment markers
- presence of specificity markers

This is not a full semantic judge. It is a deterministic benchmark harness intended to be:

- cheap
- portable
- CI-friendly
- useful as a regression layer

## How to Use This Professionally

Recommended workflow:

1. Keep this deterministic suite in CI.
2. Run candidate prompt or skill changes against it.
3. Use the JSON reports for regression tracking.
4. Layer live LLM judging or human review on top for higher-stakes releases.

## Future Extensions

Strong next steps:

1. Add pairwise model-vs-model comparisons.
2. Add rubric-based LLM-as-judge scoring.
3. Add adversarial benchmark cases.
4. Add multi-turn editorial cases:
   diagnose first, rewrite second, self-score third.
