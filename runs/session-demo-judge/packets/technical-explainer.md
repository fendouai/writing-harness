# Writing Harness Judge Packet

Case ID: technical-explainer
Title: Technical Explainer Rewrite
Surface: engineering blog paragraph
Audience: backend engineers
Task: Rewrite the paragraph so it is precise, useful, and technically credible.

Judge standard:
- authored quality over surface human-likeness
- stronger specificity
- stronger judgment
- better audience fit
- more useful language
- fewer generic, padded, or stock phrases

Preserve facts:
- - retries
- reliability

Avoid phrases:
- - it is important to note
- in today's fast-paced
- seamless user experience

LEFT candidate:
It is important to note that retries can improve reliability in modern systems. In today's fast-paced digital environment, organizations should implement retries to ensure robust performance and a seamless user experience. Different retry strategies have different pros and cons, so teams should evaluate their options carefully.


RIGHT candidate:
Retries help reliability only when you are selective about what you retry. A timeout or `429` response is usually worth another attempt with backoff. A state-changing request is different: if the operation is not idempotent, retries can duplicate work instead of fixing the failure. The practical rule is simple. Retry transient failures, not everything, and make sure write paths are safe before you automate the retry loop.


Write valid JSON to:
/Users/f/GitHub/writing-harness/runs/session-demo-judge/results/technical-explainer.json

Required JSON keys:
- winner: "left" | "right" | "tie"
- left_score: integer 0-100
- right_score: integer 0-100
- confidence: integer 1-5
- summary: short string
- strengths_left: array of strings
- strengths_right: array of strings
- risks_left: array of strings
- risks_right: array of strings
