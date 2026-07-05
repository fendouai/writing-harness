# CW-Harness v3 Upgrade Design

## Purpose

This document translates the `CW-Harness v3.0` whitepaper into an implementation plan for this repository.

The goal is not to replace `Writing Harness` with an abstract theory layer. The goal is to upgrade the repository so it can operate as a real cognitive-writing harness with:

- explicit baseline artifacts
- architecture and module planning
- deterministic sensor checks
- stage-by-stage QA gates
- module-local rollback guidance
- benchmark and judge workflows that verify both output quality and process quality

In short:

> Move the project from "rewrite + evaluate" toward "baseline -> architecture -> module spec -> draft -> unit test -> integration test -> rollback".

## Why This Upgrade Exists

The current repository already has strong foundations:

- a skill entrypoint
- structured references
- deterministic benchmark scoring
- pairwise judging
- writing lint
- trace-aware QA

What it does not yet fully encode is the deeper systems model from the whitepaper:

- reader state as a first-class baseline
- K/P/A cognitive targets
- an explicit AEH architecture
- standard module specs
- unit-test style verification by module and by cognitive dimension
- rollback advice tied to the failed dimension

This round also adds a CTA layer:

- think-aloud extraction of reader defaults
- critical-incident framing for expectation breaks
- GOMS-style decomposition for executable methods
- milestone rehearsal for temporal anchoring
- rebuttal rehearsal for identity transfer

This upgrade fills those gaps while preserving the existing practical style of the repository.

## Design Principles

### 1. Theory must become artifacts

Every major whitepaper concept must become a file, schema, metric, or script output.

### 2. The harness stays CI-friendly

The repository should continue to support deterministic local checks without requiring a hosted API.

### 3. Process quality matters as much as output quality

A candidate rewrite is stronger when it is accompanied by a credible:

- baseline
- module plan
- rewrite trace
- self-evaluation
- CTA elicitation payload

### 4. Keep the entrypoint compact

The `SKILL.md` file should remain a steering layer. The heavier process details should live in references and scripts.

## New System Model

The upgraded repository adopts the following operating model:

### L1. Requirements and Baseline

Capture the reader's cognitive starting state and target state as K/P/A coordinates.

Required artifact:

- `baseline report`

### L2. Architecture and Design

Select a cognitive architecture pattern.

Default pattern:

- `Assert -> Exception -> Handler -> Log`

Required artifacts:

- `architecture blueprint`
- `module specification`

### L3. Execution and Encoding

Generate the writing as an ordered sequence of modules.

Default standard module path:

- `M-01 old-belief index`
- `M-02 expectation break`
- `M-03 new framework`
- `M-04 boundary and timing anchor`
- `M-05 identity embed`

Required artifacts:

- `rewrite output`
- `trace output`

### L4. Monitoring and Observation

Evaluate the output with deterministic sensors, stage gates, and rollback advice.

Required artifacts:

- `unit test report`
- `integration report`
- `rollback advice`

## Repository Changes

### 1. New cognitive artifact schema

Each benchmark or agent-native run should be able to emit a sidecar JSON artifact with:

- `baseline`
- `architecture`
- `modules`
- `trace`
- `unit_tests`
- `integration`
- `rollback`

This can live next to the candidate text as:

- `case-id.cw.json`

The existing `.trace.json` format remains useful, but it is too narrow for the new system because it lacks:

- K/P/A baseline coordinates
- architecture choice
- module-level specs
- explicit gate outcomes

### 2. New deterministic cognitive sensors

The repository should add mechanical checks for the whitepaper's K/P/A dimensions.

#### K sensors

- concept distinction precision
- observable action verb density
- boundary-marking phrases

#### P sensors

- if-then density
- tool/template delivery
- ordered process cues

#### A sensors

- attribution shift
- resistance drop estimate
- identity / agency language

### 3. New module-spec aware QA

Each candidate should support module-aware checks:

- does M-01 index old beliefs
- does M-02 create a credible exception or contradiction
- does M-03 provide a usable decision tool
- does M-04 anchor timing, boundaries, or next checkpoints
- does M-05 provide identity, memory, or behavior lock-in

### 4. New rollback logic

The harness should offer deterministic rollback advice by failed dimension:

- `K failure -> revisit M-01/M-02`
- `P failure -> revisit M-03`
- `A failure -> revisit M-04/M-05`

## New Artifact Contract

### `baseline report`

```json
{
  "reader": "target audience",
  "starting_state": {
    "K": "current misconception or blur",
    "P": "current bad process",
    "A": {
      "emotion": "initial state",
      "resistance": 7,
      "attribution": "external"
    }
  },
  "target_state": {
    "K": "new distinctions and boundaries",
    "P": "new process or tool",
    "A": {
      "emotion": "target state",
      "resistance": 3,
      "attribution": "internal"
    }
  },
  "displacement": {
    "K": "what concept must change",
    "P": "what process must change",
    "A": "what attitude must change"
  }
}
```

### `architecture blueprint`

```json
{
  "pattern": "AEH",
  "layers": {
    "assert": "index old beliefs",
    "exception": "break old expectations",
    "handler": "install new model and tool",
    "log": "anchor behavior and identity"
  }
}
```

### `module specification`

```json
{
  "modules": [
    {
      "id": "M-01",
      "name": "old-belief-index",
      "ksa_targets": ["K", "A"],
      "input_state": "...",
      "logic": ["name 3 misconceptions"],
      "output_state": "...",
      "interface_hook": "transition sentence"
    }
  ]
}
```

### `cw artifact`

```json
{
  "baseline": {},
  "architecture": {},
  "modules": [],
  "trace": {},
  "unit_tests": {},
  "integration": {},
  "rollback": {}
}
```

## Script-Level Upgrade Plan

### `scripts/writing_checks.py`

Expand the shared check layer so it can score:

- K/P/A sensors
- module presence
- AEH phase completeness
- rollback mapping

### `scripts/run_writing_lint.py`

Keep the existing lint behavior, but add an optional `--cw-json` mode that checks a full cognitive artifact rather than only prose.

### `scripts/run_writing_harness_benchmarks.py`

Upgrade benchmark scoring to include:

- writing lint
- genre contracts
- K/P/A sensor checks
- module-coverage checks
- cognitive artifact completeness

### `scripts/prepare_agent_native_benchmark_run.py`

Upgrade benchmark packets to request:

- final rewrite
- full cognitive artifact sidecar

Not just:

- final rewrite
- trace

### `scripts/prepare_agent_native_judge_run.py`

Upgrade judge packets so the judge can compare:

- final article quality
- process quality
- module discipline
- baseline credibility
- rollback readiness

### `scripts/summarize_agent_native_judgments.py`

Upgrade the output to summarize:

- text winner
- trace winner
- cognitive-process winner
- QA completeness

## Skill and Reference Upgrades

### Skill entrypoint

The skill should explicitly acknowledge a six-stage execution model:

1. baseline
2. architecture
3. module spec
4. draft
5. unit test
6. integration and rollback

### New reference files

Add structured reference material for:

- `cognitive-baseline.md`
- `aeh-architecture.md`
- `module-specs.md`
- `cognitive-sensors.md`
- `rollback-policy.md`

These should be referenced from `SKILL.md`, not fully duplicated into it.

## Test Plan

### Deterministic validation

Run:

- lint checks
- harness artifact checks
- benchmark sanity checks
- gold benchmark evaluation
- candidate benchmark evaluation
- packet-generation smoke tests
- judge summary QA checks

### New cognitive validation

Add checks that verify:

- sample cognitive artifacts are parseable
- K/P/A metrics can be computed
- rollback advice is produced when a dimension fails
- packet generation includes baseline, module, and rollback fields

## Migration Strategy

### Phase 1

Introduce the new document and schemas without breaking existing flows.

### Phase 2

Upgrade benchmark and judge scripts to accept both:

- legacy `.trace.json`
- new `.cw.json`

### Phase 3

Prefer `.cw.json` in all generated packets and sample runs.

## Definition of Done

This upgrade is complete when:

- the repository contains a professional implementation document
- the skill and references describe the cognitive pipeline clearly
- benchmark packets request a cognitive artifact sidecar
- benchmark scoring uses K/P/A and module-aware checks
- judge packets and summaries are cognitive-process aware
- sample runs contain valid sidecars
- the deterministic suite still passes

## One-Line Summary

The upgraded repository should treat writing as a deterministic cognitive-state transition system:

> define the reader baseline, choose an architecture, design modules, generate the draft, test the state transition, and rollback only the failed layer.
