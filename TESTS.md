# Tests: historywright

Test runs for [README.md](README.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261017-5 · 2026-10-17 · evergreen.py worth --ab, sonnet, cache cleared first · Windows 11 dev machine · action-wikidata-full-statements with 3/3, without 0/3
- With a clean cache, every with run read Wikidata full statements (wd claims / wbgetclaims) before answering; the without arm never did. action-cache-entry did not run (the second call's --case matched nothing): still owed.
- led to: none

### T-20261017-4 · 2026-10-17 · evergreen.py worth --ab, sonnet, 3 runs per arm, research tools granted to both arms · Windows 11 dev machine · with 27/33, without 13/33
- A/B: pass 82% with, 39% without, +42 points (noise margin 22); cost x3.09, turns x3.68, time x4.77. Harness verdict TRIM.
- Outcome cases with the skill: caesar 3/3 (without 0/3: no Mommsen/102 BC), kangxi 3/3 (without 0/3: no Qianlong to 1799), microsoft 3/3 (without 0/3: no Albuquerque), five-books 3/3 (1/3), menelik 3/3 (2/3), citogenesis 3/3 (2/3), misattributed-quote 3/3 (3/3, redundant), october-revolution 3/3 (3/3, redundant).
- action-validate-pack 3/3 (without 2/3). action-wikidata-full-statements 0/3 and action-cache-entry 0/3 in both arms · harness · the with runs ran `cache get`, found an answer an earlier eval run had saved in the shared ~/.historywright/cache, and stopped as Step 0 says; re-run separately after clearing the cache (next entry).
- Side effects: eval runs wrote 10 cache entries to the real cache (moved to ~/.historywright/cache-from-evals-2026-10-17/); no repository files changed.
- led to: L-005; evals/evals.json tools field

### T-20261017-3 · 2026-10-17 · evergreen.py worth --ab, sonnet, 3 runs per arm, default tools · Windows 11 dev machine · with 16/33, without 11/33 (environment)
- A/B: 48% with, 33% without, verdict CUT, but the with arm measured the permission gate: the runner's default outcome tools exclude shell and web, so hw.py, WebFetch and WebSearch came back "requires approval" and the skill refused to answer from memory (its rule), while the without arm answered from memory in 3 to 5 s. Not counted as a verdict.
- led to: L-005

### T-20261017-2 · 2026-10-17 · claude plugin eval 2.1.x, --ablation none, sonnet judge · Windows 11 dev machine · triggers 15/15, decoys 9/9
- trigger-caesar, -emperor, -microsoft (historywright), trigger-sources (historywright-sources) and trigger-pack (historywright-pack): 3/3 each. decoy-story, decoy-pdf (readwright's job), decoy-news: 0 invocations in 3/3 each. Cost $2.05.
- led to: none

### T-20261017-1 · 2026-10-17 · offline unit tests and CI · Windows 11 + GitHub Actions (Linux, macOS, Windows; Python 3.9, 3.14) · 31/31
- `tests/test_hw.py` (HTTP from recorded fixtures) and `tests/check_skills.py` pass on all six CI jobs: the cross-OS check for hw.py.
- led to: none
