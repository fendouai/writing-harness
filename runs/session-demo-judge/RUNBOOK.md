# Agent-Native Judge Session Runbook

Use this runbook in a single agent session.

## Goal

Process every judge packet and write one valid JSON judgment per case.

## Session Files

- Manifest: /Users/f/GitHub/writing-harness/runs/session-demo-judge/judge-manifest.json
- Packets directory: /Users/f/GitHub/writing-harness/runs/session-demo-judge/packets
- Results directory: /Users/f/GitHub/writing-harness/runs/session-demo-judge/results

## Instructions For The Agent

1. Read the manifest first.
2. Process every packet in the packets directory.
3. For each packet:
   - compare LEFT vs RIGHT
   - produce valid JSON with the required keys
   - write the JSON to the requested result file
4. Do not skip cases.
5. Do not write prose outside the JSON result files.
6. After finishing all cases, stop and report completion.

## Suggested user message

Complete the pairwise Writing Harness judge session described in:
/Users/f/GitHub/writing-harness/runs/session-demo-judge/RUNBOOK.md

Make sure every packet in /Users/f/GitHub/writing-harness/runs/session-demo-judge/packets is processed and every JSON result is written into /Users/f/GitHub/writing-harness/runs/session-demo-judge/results.
