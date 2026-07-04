# Writing Harness Eval System

This directory defines a practical test system for the Writing Harness.

It is inspired by harness-engineering practice collected in:

- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

The design goal is simple:

> Treat writing quality as a harness problem, not a one-shot prompting problem.

## Why This Exists

A writing harness is only useful if it can be tested.

Without tests, a writing harness tends to drift in familiar ways:

- the entrypoint becomes bloated
- references lose structure
- the skill stops steering and starts rambling
- evaluation criteria become vague
- rewrites become "better sounding" without becoming better

This eval system is designed to catch those failures early.

## Test Layers

This repo uses two layers of tests.

### 1. Artifact Integrity Tests

These are fully automated and run now.

They verify that the repository contains the expected harness components:

- a short top-level guide
- a compact skill entrypoint
- structured reference files
- explicit guides and sensors
- a rubric
- a failure taxonomy
- prompt templates

They also verify that the harness preserves key architectural ideas:

- authored quality over surface humanization
- short entrypoint plus deeper references
- guides and sensors as separate concerns
- iterative evaluation, not one-pass generation

### 2. Behavioral Coverage Tests

These are also automated, but they test capability coverage rather than full model execution.

Each scenario defines the capabilities the harness must support, such as:

- extracting a thesis
- identifying generic abstraction
- strengthening judgment
- increasing specificity
- applying the rubric

The runner checks whether the current harness artifacts contain evidence of these capabilities.

This is not a substitute for live model evals. It is a regression layer for the harness itself.

## Why Not Only Use Live LLM Evals

Live model evals are important, but they are not enough by themselves.

For an open-source harness project, you also want tests that are:

- deterministic
- cheap to run
- usable in CI
- independent of a specific model provider

That is why this system starts with artifact and coverage tests.

You can later add live execution evals on top of it.

## Current Files

```text
evals/
├── README.md
├── benchmarks/
│   ├── README.md
│   ├── cases.json
│   └── gold/
├── cases/
│   └── behavioral-coverage.json
└── reports/
```

```text
scripts/
├── run_writing_harness_benchmarks.py
└── run_writing_harness_evals.py
```

## Running the Eval Suite

From the repository root:

```bash
python3 scripts/run_writing_harness_evals.py
```

To save a machine-readable report:

```bash
python3 scripts/run_writing_harness_evals.py --json evals/reports/latest.json
```

To run the end-to-end benchmark suite:

```bash
python3 scripts/run_writing_harness_benchmarks.py --sanity
python3 scripts/run_writing_harness_benchmarks.py --use-gold
```

## What Counts as a Pass

The suite is currently opinionated but conservative.

A healthy Writing Harness should:

- pass all artifact integrity checks
- pass all behavioral coverage checks
- produce a reusable JSON report

If the suite fails, treat the result as a harness bug, not a documentation style preference.

## Benchmark Layer

The benchmark suite extends this system from harness integrity to end-to-end rewrite testing.

It adds:

- realistic rewrite tasks
- gold outputs
- a deterministic scorer
- candidate directory evaluation
- prompt-packet generation for model runs
- agent-native benchmark packets
- agent-native pairwise judge packets

See [`evals/benchmarks/README.md`](/Users/f/GitHub/humanize-text-guide/evals/benchmarks/README.md).
