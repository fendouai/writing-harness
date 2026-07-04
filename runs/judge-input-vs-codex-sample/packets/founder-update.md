# Writing Harness Judge Packet

Case ID: founder-update
Title: Founder Update Rewrite
Surface: founder note
Audience: startup team and early investors
Task: Rewrite the update so it sounds observed and decisive, not polished and empty.

Judge standard:
- authored quality over surface human-likeness
- stronger specificity
- stronger judgment
- better audience fit
- more useful language
- fewer generic, padded, or stock phrases

Preserve facts:
- - customer
- onboarding
- pricing

Avoid phrases:
- - productive week
- learned a lot
- product direction
- strong opportunities
- iterating thoughtfully

LEFT candidate:
We had a productive week and learned a lot from customer conversations. Users are excited about the product direction, and we see strong opportunities to improve the onboarding experience and pricing communication. Going forward, we will continue iterating thoughtfully based on feedback.


RIGHT candidate:
Customer conversations this week clarified one issue faster than any dashboard could: the product is landing, but the pricing story is not. People are getting through onboarding, then hesitating because they are unsure what they would pay and when. The next move is not more feature work. It is tighter pricing communication and a simpler self-serve path at sign-up.


Write valid JSON to:
/Users/f/GitHub/writing-harness/runs/judge-input-vs-codex-sample/results/founder-update.json

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
