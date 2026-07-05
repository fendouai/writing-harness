# AEH × CTA Bridge

Use this when the architecture feels too abstract or too crowded.

This file exists to reduce the whole system to one simple relation.

## The Core Split

- `AEH` is the macro route
- `M-01` to `M-05` are the execution containers
- `CTA` is the micro elicitation engine inside those containers
- `Sensors` decide whether the move worked

That means:

- `AEH` answers:
  - What cognitive path should the reader travel?
- `Modules` answer:
  - Where does each part of that travel happen?
- `CTA` answers:
  - What hidden expert move is being extracted and installed inside each part?
- `Sensors` answer:
  - Did the installation succeed?

## In One Table

| Layer | Job | Question |
| :--- | :--- | :--- |
| `Baseline` | define reader start/end state | What must change? |
| `AEH` | define the cognitive route | In what order should it change? |
| `M-01..M-05` | define execution containers | Where is each move implemented? |
| `CTA` | extract expert decision scripts | What exactly does the reader learn to notice, reject, and do? |
| `Sensors` | validate the move | Did the change actually happen? |
| `Rollback` | local repair | Which layer failed? |

## Why This Matters

Without `AEH`, the system has no route.

Without `Modules`, the route is too vague to execute.

Without `CTA`, the modules explain but do not transfer expert judgment.

Without `Sensors`, the whole thing collapses back into taste.

## The One-Line Version

> AEH decides the route. Modules hold the work. CTA sharpens the move. Sensors decide if it worked.
