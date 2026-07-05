# Rollback Policy

Use this when a draft fails its unit or integration checks.

Do not rewrite the whole piece by default.

## Rollback Mapping

- `K` failure:
  revisit `M-01` and `M-02`
- `P` failure:
  revisit `M-03`
- `A` failure:
  revisit `M-04` and `M-05`

## What To Preserve

When rolling back one dimension:

- lock the unaffected modules
- change the smallest region that can fix the failed sensor
- keep the central claim stable unless it is the root cause

## Examples

- If the piece is still vague about the new distinction, repair the belief-index and expectation-break layers first.
- If the piece sounds smart but gives no usable path, repair the framework layer.
- If the piece is accurate but leaves the reader passive, repair the timing anchor and identity embed layers.
