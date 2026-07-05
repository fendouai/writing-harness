---
name: writing-harness
description: Use when rewriting, evaluating, or generating text for authored quality rather than merely human-like style. Applies a spec, rewrite workflow, rubric, and failure taxonomy to make AI-assisted writing clearer, more specific, more judged, and more useful.
---

# Writing Harness

Writing Harness is a quality-first writing skill.

Treat this file as the entrypoint, not the full manual.

Use it to steer the agent toward the right process, then load the reference files as needed. The durable system of record lives under `references/`.

Use it when the user wants to:

- humanize AI-generated writing
- improve a rough draft
- make text sound less generic
- build stronger prompts for writing quality
- evaluate drafts with a rubric
- create a repeatable rewrite workflow
- turn AI output into publishable prose

Do not optimize for detector evasion. Do not add fake mistakes, fake personality, or random slang. Optimize for authored quality.

## Core Principle

Do not aim for "more human-like" by default.

Aim for writing that feels:

- authored
- specific
- useful
- judged
- credible

The target is strong writing, not plausible surface imitation.

## Harness Framing

The harness has two parts:

- guides, which shape the work
- sensors, which evaluate the work

In this skill:

- guides include the spec, rewrite workflow, and prompt templates
- sensors include the rubric, failure taxonomy, and meta checks

Do not treat a fluent draft as a successful draft unless the sensors agree.

## Use When

- The draft is fluent but generic
- The user says the text feels too AI-generated
- The user wants a better prompt for writing quality
- The user wants a rewrite system, rubric, or harness
- The text needs more point of view, structure, or specificity

## Do Not Use When

- The user wants factual research but has not provided source material and the topic is time-sensitive
- The task is pure proofreading with no need for rewrite judgment
- The user only wants detector evasion tactics

## Workflow

Follow this sequence:

### 1. Build the spec

Before rewriting, identify or infer:

- target reader
- reader starting point
- piece objective
- required tone range
- desired conviction level
- what the piece must accomplish
- what it must avoid

If needed, ask for missing high-impact context. Otherwise infer and proceed.

### 2. Set the cognitive baseline

If the task is trying to change the reader's mind, define the reader's K/P/A starting state and target state.

Use `references/cognitive-baseline.md`.

### 3. Identify the central claim

Before editing line by line, state:

- the main point
- what should be cut
- what deserves emphasis

If the piece has no real thesis, say so and propose one before rewriting.

### 4. Diagnose failure modes

Check the draft for:

- generic abstraction
- empty setup
- over-explanation
- false balance
- stock phrases
- weak or missing examples
- invisible speaker
- uniform rhythm
- padded ending

Use the taxonomy in `references/failure-taxonomy.md`.

### 5. Choose an architecture and module path

For cognitive-change tasks, use AEH plus the standard module path.

Use:

- `references/aeh-architecture.md`
- `references/module-specs.md`

### 6. Rewrite for authored quality

Rewrite toward:

- stronger specificity
- clearer priority
- better reader fit
- more credible voice
- more useful insight
- less template energy

Make the text sound like someone with a perspective is writing to someone specific for a reason.

### 7. Evaluate the result

Score the result with the rubric in `references/rubric.md`.

If the rewrite is still weak on core dimensions, revise again instead of presenting a shallow cleanup as done.

### 8. Iterate through the loop

Use the sensors to decide whether the draft is done.

If the result is still generic, over-explained, or low-judgment, continue the loop:

- diagnose
- revise
- re-score

Do not stop at a smoother version of the same weak draft.

## Rewrite Rules

- Cut generic sentences that could fit almost any article
- Replace abstraction with examples, constraints, stakes, or consequences
- Strengthen judgment where the text hides behind balance
- Keep structure only when it serves the reader
- Preserve necessary precision for technical or professional writing
- Prefer clarity over flourish
- Do not inject fake anecdotes or invented experience

## Knowledge Loading

Load only what is needed:

- `references/rewrite-workflow.md`
  For full rewrites and process design.
- `references/rubric.md`
  For evaluation and iteration.
- `references/failure-taxonomy.md`
  For diagnosis.
- `references/prompt-templates.md`
  For reusable prompts and harness setup.
- `references/cognitive-baseline.md`, `references/aeh-architecture.md`, `references/module-specs.md`, `references/cognitive-sensors.md`, `references/rollback-policy.md`
  For cognitive-state transition work, module QA, and rollback design.

Keep the skill compact. Pull deeper detail from references instead of expanding this file into a monolith.

## Suggested Output Modes

Choose the lightest mode that satisfies the request.

### Light Rewrite

Use when the user wants quick cleanup.

Output:

- revised text
- optional 2-4 bullet note on what changed

### Editorial Rewrite

Use when the user wants a stronger transformation.

Output:

- revised text
- short diagnosis
- top failure modes fixed

### Harness Review

Use when the user wants a system, not just a rewrite.

Output:

- spec
- diagnosis
- rewrite strategy
- rubric score
- next-pass recommendations

## Default Prompting Frame

When asked to rewrite, use this mental frame:

"Do not optimize for casualness or fake humanity. Optimize for authored quality: clear intent, audience awareness, concrete detail, editorial judgment, credible voice, and reader usefulness."

## Success Condition

The task is complete when the output is not only more natural, but materially better on the core sensors:

- clearer purpose
- better audience fit
- stronger point of view
- more specificity
- higher usefulness
- more credible voice
