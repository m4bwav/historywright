# Measured claims in sources.json (2026-11-01)

Small ruling, made without asking (owner's rule: decide small rulings and flag them).

- Shape: a claim with `measured: {scale, how}` and a `locator` (the sheet) instead of a `quote`.
- Why not a new source `kind`: the source is still primary (the drawing); only the claim differs, and one
  sheet can hold both quoted notes and measured values.
- A measured claim is not a quote check: `verify sources` lists it with `match: measured` and `found: null`,
  so nothing claims the value was stated. Corroboration counting is unchanged.
- A claim with both `quote` and `measured` is checked as a quote (the quote is the stronger evidence).
