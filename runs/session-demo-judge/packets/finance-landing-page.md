# Writing Harness Judge Packet

Case ID: finance-landing-page
Title: Finance Landing Page Rewrite
Surface: landing page copy
Audience: finance teams
Task: Rewrite the copy so it sounds like it understands the real close process instead of sounding like generic B2B software marketing.

Judge standard:
- authored quality over surface human-likeness
- stronger specificity
- stronger judgment
- better audience fit
- more useful language
- fewer generic, padded, or stock phrases

Preserve facts:
- - finance teams
- ERP
- spreadsheets

Avoid phrases:
- - innovative platform
- empowers
- seamless automation
- world-class visibility
- strategic outcomes

LEFT candidate:
Our innovative platform empowers finance teams to transform their close process with seamless automation and world-class visibility. It integrates with your ERP and spreadsheets to unlock efficiency, reduce friction, and drive strategic outcomes across the organization.


RIGHT candidate:
Finance teams do not need more “visibility.” They need a close process that stops depending on scattered spreadsheets and last-minute ERP checks. This product helps teams reconcile faster, see what is blocked, and move approvals without the usual month-end chase across files, tabs, and follow-up messages.


Write valid JSON to:
/Users/f/GitHub/writing-harness/runs/session-demo-judge/results/finance-landing-page.json

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
