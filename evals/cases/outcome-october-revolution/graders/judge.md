---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- gives 25 October 1917 Old Style (Julian) and 7 November 1917 New Style (Gregorian), and says why both exist
- the conversion is computed (hw.py cal) or quoted from a fetched source, not asserted from memory
FAIL if any is missing or contradicted.
