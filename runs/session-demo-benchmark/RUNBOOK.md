# Agent-Native Benchmark Session Runbook

Use this runbook in a single agent session.

## Goal

Process every benchmark packet with the Writing Harness skill and write one final rewrite per case.

## Session Files

- Manifest: /Users/f/GitHub/writing-harness/runs/session-demo-benchmark/run-manifest.json
- Packets directory: /Users/f/GitHub/writing-harness/runs/session-demo-benchmark/packets
- Results directory: /Users/f/GitHub/writing-harness/runs/session-demo-benchmark/results

## Instructions For The Agent

1. Use the Writing Harness skill.
2. Read the manifest first.
3. Process every packet in the packets directory.
4. For each packet:
   - read the case instructions
   - produce one final rewrite
   - write the final text to the requested result file
5. Do not skip cases.
6. Do not write commentary into the result files.
7. After finishing all cases, stop and report completion.

## Suggested user message

Use the Writing Harness skill and complete the benchmark session described in:
/Users/f/GitHub/writing-harness/runs/session-demo-benchmark/RUNBOOK.md

Make sure every packet in /Users/f/GitHub/writing-harness/runs/session-demo-benchmark/packets is processed and every output is written into /Users/f/GitHub/writing-harness/runs/session-demo-benchmark/results.
