# Writing Harness Judge Packet

Case ID: internal-memo
Title: Internal Memo Rewrite
Surface: internal memo
Audience: engineering leadership
Task: Rewrite the memo so it makes a recommendation instead of hiding behind balance.

Judge standard:
- authored quality over surface human-likeness
- stronger specificity
- stronger judgment
- better audience fit
- more useful language
- fewer generic, padded, or stock phrases

Preserve facts:
- - engineering handbook
- runbooks
- Notion
- Markdown

Avoid phrases:
- - several valid options
- offer benefits
- consider tradeoffs carefully

LEFT candidate:
There are several valid options for where we keep our engineering handbook and runbooks. Notion is familiar to more teams, while Markdown in the repository has advantages for version control and discoverability. Both approaches offer benefits, and we should consider tradeoffs carefully before making a final decision.


RIGHT candidate:
We should keep the engineering handbook and runbooks in Markdown in the repository, and use Notion for lighter collaboration that does not need to be the source of truth. The docs that explain how the system works need version control, review history, and code-adjacent discoverability. If those operating docs live outside the repo, they will drift faster and become less trustworthy.


Write valid JSON to:
/Users/f/GitHub/writing-harness/runs/session-demo-judge/results/internal-memo.json

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
