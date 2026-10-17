# Creation pass 2026-10-17: testing (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-17 (live read) · Wikidata's Caesar record has the dispute built in, and a plain truthy query hides it
- What: `wbgetclaims Q1048 P569` returns four statements. The preferred one is `-0100-07-12`, but at month precision (10), with earliest 12 July and latest 13 July qualifiers, P1480 = Q18912752 "disputed", and proleptic Julian calendar. Three normal-rank statements follow: 13 July 100 BC at day precision (two books, one quoting "13 July 100 BCE according to the modern calendar"); 102 BC at year precision, flagged disputed and sourced to JSTOR 295588 (Rice Holmes, JRS 1917, "Was Caesar born in 100 or in 102 BC?"); and 100 BC at year precision under the *Gregorian* model (from DPRR), which contradicts the others. The WDQS manual says `wdt:` returns best-rank ("truthy") values only, so a `wdt:P569` query shows just the preferred value and loses the 102 BC dispute. Scholarship confirmed through Cambridge/JSTOR abstracts: Mommsen argued for 102, Badian (1959) and Deutsch (1914) for 100, and the consensus is 100 BC. The 12/13 July split comes from the Ludi Apollinares clash.
- Track: testing
- Affects: the Caesar outcome case (gold) and the hw.py Wikidata query
- Magnitude: n/a (initial)
- Suggested response: adopt. hw.py queries `p:/ps:/psv:` with `wikibase:timePrecision`, `wikibase:timeCalendarModel`, rank and P1480, never `wdt:` alone. Add an action case: the trace regex matches `psv:P569|p:P569|wbgetclaims`, with a `not_contains`-style check against a lone `wdt:P569`. Outcome rubric: (a) 100 BC as the standard year; (b) 12 or 13 July, with the other day named; (c) 102 (or 101) BC named as the alternative; (d) attributed to Mommsen or to "some scholars, from the ages at which he held office"; (e) the reason given, i.e. the cursus ages, not just "sources differ". Also a decoy-like guard: the answer must not claim a Gregorian date for 100 BC as exact, because the date falls before the Julian reform and the Julian calendar is proleptic here.
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1048&property=P569&format=json, https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual, https://resolve.cambridge.org/core/journals/journal-of-roman-studies/article/was-caesar-born-in-100-or-in-102-bc/BDE639D70E0F8A3A819F268D2E827975

### F2 · 2026-10-17 (live read) · Microsoft gold confirmed, with one source only
- What: Q2283 P571 = `+1975-04-04`, day precision, Gregorian, normal rank. Its single reference is a Microsoft Spain 40th-anniversary post (news.microsoft.com/es-es, 2015-04-06), so it is an official source. Secondary sources agree: Gates and Allen, Albuquerque, a partnership. One secondary source dates the "Micro-Soft" name registration in New Mexico to 26 Nov 1976, which gives a "which founding?" ambiguity (partnership, name registration, later incorporation; the incorporation date was not verified in this pass).
- Track: testing
- Affects: the Microsoft outcome case
- Magnitude: n/a (initial)
- Suggested response: adopt. Regex gold `4 April 1975|April 4, 1975|1975-04-04`, plus `Allen` and `Albuquerque`. The rubric accepts a mention of the later registration or incorporation and fails an answer that gives 1976 or 1981 as *the* founding date. The citation must resolve to a microsoft.com host or another primary source (see F5).
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q2283&property=P571&format=json, https://en.wikipedia.org/wiki/History_of_Microsoft

### F3 · 2026 (current docs) · `claude plugin eval` can mock the source APIs and pin network domains
- What: There are six graders: `regex` (targets `last_message`, `trace`, `{source: file, path}`, `mock_calls`; JS regex with `match: not_contains|count:N`), `tool_used` (`tool`, `input_match`, `min`, `max`), `tool_order` (`before`, `after`), `file_exists` (only files created in the run), `llm`, and `baseline`. There are no code graders. Mock MCP servers (`evals/mocks/<server>/<tool>.md`, with an `expect:` input guard and `{{file:fixtures/...}}` substitution) return fixed answers, and `type: agent` mocks can be replayed from `mocks/.replay/`. WebFetch and WebSearch are removed unless granted. Granting Bash requires an OS sandbox (none on native Windows, so use WSL2), and network is limited to domains granted as `WebFetch(domain:...)`. The docs advise one grader on the result and one on the path taken.
- Track: testing
- Affects: the harness choice and the action cases
- Magnitude: n/a (initial)
- Suggested response: adopt. Action case "evidence outside transcript": `tool_used` Bash with `input_match` `hw\.py (wd|wikidata)` or WebFetch with `query\.wikidata\.org|wikidata\.org/w/api`, plus `tool_order` (fetch before the answer file is written). Run with `--allow-tools "Bash(python *hw.py*)" "WebFetch(domain:www.wikidata.org)" "WebFetch(domain:query.wikidata.org)"` under WSL2, or through `EG worth --ab` on Windows. Fixture the Q1048 JSON from F1 so the Caesar case is deterministic. The cache case uses `file_exists` on the cache path, or since the cache lives in `~/.historywright/`, outside the workspace, a `regex` on a workspace copy or `HW_HOME` override (hw.py should honour an env var for this).
- Sources: https://code.claude.com/docs/en/plugin-evals

### F4 · 2026-06 · DRIFT / TELBench: audit claims against the trajectory
- What: A claim-centric audit that checks whether each claim in the answer is supported by evidence in the agent's own trajectory, with TELBench (1,000 instances) for locating error spans such as failed searches. It is the closest published method for catching "narrated a search it never ran". Read from a search snippet only, not fetched.
- Track: testing
- Affects: the action cases (narrated-search failure)
- Magnitude: n/a (initial)
- Suggested response: note. The cheap version to adopt: every URL in answer.md/sources.json must appear in a WebFetch input or hw.py output in the trace (regex per URL, or a `hw.py verify-pack --trace` check).
- Sources: https://papers.cool/arxiv/2606.02060

### F5 · 2026-05-07 · "Cited but Not Verified": live links are not the hard part, support is
- What: Three binary metrics per citation: Link Works (HTTP, no LLM), Relevant Content (an LLM judge on the first 5,000 characters) and Fact Check (an LLM judge; uncertain counts as fail). Frontier models keep links above 94% and relevance above 80%, but Fact Check scores only 39 to 77% (Claude Opus 4.5 highest at 76.8%). Fact Check falls about 42% on average as tool calls grow from 2 to 150 (Opus 4.6 went from 80.0 to 57.9%). Providers that cite more score worse.
- Track: testing
- Affects: the outcome cases; hw.py `verify`
- Magnitude: n/a (initial)
- Suggested response: adopt. Add a quote-span check: sources.json stores, per claim, the exact supporting `quote`. hw.py re-fetches the page (or reads the cached copy) and checks the quote is a normalised substring. A missing quote fails, as does a date in the quote that differs from the claim. Grade relevance and support separately, and treat "uncertain" as fail.
- Sources: https://arxiv.org/html/2605.06635v1

### F6 · 2026-04-03 · Reference hallucination rates and the urlhealth check
- What: 3 to 13% of cited URLs from 10 models and agents (53,090 URLs, DRBench) were hallucinated, meaning no Wayback snapshot ever existed. Deep-research agents run 10.7%, search-augmented models 4.8%. Their verifier, urlhealth (an 83-line Python package, also an agentskills.io skill), uses HEAD, falls back to GET on 405/403/501, and on a 404 checks the Wayback availability API. It labels each URL LIVE, DEAD (404 with a snapshot), LIKELY_HALLUCINATED (404, no snapshot) or UNKNOWN (403, 429, timeouts). Used as a self-correction tool it cut non-resolving URLs below 1% (Sonnet 4.5: 4.9 to 0.8%). No repository URL appears in the paper; a search for "urlhealth" found nothing, so it may be unreleased. DOIs are not checked.
- Track: testing
- Affects: hw.py `verify`; a case in evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt the method, which is about 40 stdlib lines (urllib plus `archive.org/wayback/available`), not the package. Add a DOI check (`https://doi.org/<doi>` resolves, or the Crossref/OpenAlex API returns the work) and a QID check (`wbgetentities` returns the entity with a matching label). Eval case: the pack's sources.json has zero LIKELY_HALLUCINATED and DEAD entries and UNKNOWN at most 20%. Make re-proposing a flagged URL a failure.
- Sources: https://arxiv.org/html/2604.03173v1

### F7 · 2026-03-10 (v2) · SimpleQA Verified grader: the model for single-fact grading
- What: Answers are graded CORRECT, INCORRECT or NOT_ATTEMPTED by a gpt-4.1 autorater; the score is F1 of overall-correct and correct-given-attempted. A hedge counts only if it commits to one candidate. Listing several without committing is NOT_ATTEMPTED; committing to a wrong one is INCORRECT. Questions whose sources conflicted were *removed*, so the benchmark shows how not to grade disputes. Data, grader and leaderboard are on Kaggle.
- Track: testing
- Affects: the outcome cases (Kangxi, Microsoft); the baseline
- Magnitude: n/a (initial)
- Suggested response: adopt the three-way grade and the commit rule for the undisputed cases (Kangxi must commit to Kangxi). For disputed cases use a separate rubric (F1, F12), because SimpleQA's rule would mark "100 BC, though some argue 102" correct only if it commits, which is what the skill should do anyway. Point at the Kaggle set as an optional baseline probe; it is not history-specific.
- Sources: https://arxiv.org/html/2509.07968v2, https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified

### F8 · 2026-01 · DeepHalluBench: hallucination across the whole research trajectory
- What: Audits hallucinations along the full trajectory of a deep-research agent, not only the final answer, and finds no agent reliably clean. Known from the abstract only.
- Track: testing
- Affects: none directly
- Magnitude: n/a (initial)
- Suggested response: note
- Sources: https://arxiv.org/html/2601.22984v1

### F9 · 2025-12 / 2026-01 · FACTS suite replaces FACTS Grounding
- What: Google DeepMind's FACTS leaderboard has four parts: Parametric (closed-book), Search (with a search API), Multimodal and Grounding v2. It has 3,513 examples, public and private splits on Kaggle, and is judged by models. The Parametric vs Search split mirrors historywright's baseline-vs-skill design.
- Track: testing
- Affects: the baseline case framing
- Magnitude: n/a (initial)
- Suggested response: note. Too large and API-bound for a small suite; cite it as precedent for the memory-vs-search comparison.
- Sources: https://arxiv.org/html/2512.10791v1, https://www.infoq.com/news/2026/01/facts-benchmark-suite

### F10 · 2025 · Full fact-checking pipelines are too heavy for this suite
- What: SAFE/LongFact (google-deepmind/long-form-factuality: 695 stars, not archived, no releases, needs OpenAI/Anthropic keys and a search backend). VeriScore (Serper Google Search, about 60 calls per response) and VeriFastScore (EMNLP Findings 2025, a fine-tuned 8B model, 6.6x faster). FActScore (2023, `pip install factscore`, Wikipedia knowledge source; no successor found). AVeriTeC 2025 (FEVER at ACL 2025; open-weights systems, winner CTU AIC at 33.17%). BrowseComp-Plus (fixed 100,195-document corpus, ACL 2026) is the reproducible variant of BrowseComp.
- Track: testing
- Affects: none (the harness choice)
- Magnitude: n/a (initial)
- Suggested response: note. Borrow the *pattern* (split into atomic claims, retrieve, verify each claim, F1@K) for an optional `llm` grader. Borrow BrowseComp-Plus's idea of a fixed corpus as the reason to keep the eval fixtures as mocks (F3). None of them runs offline in a small suite.
- Sources: https://github.com/google-deepmind/long-form-factuality, https://preview.aclanthology.org/new-sigs/2025.findings-emnlp.491/, https://arxiv.org/pdf/2305.14251, https://arxiv.org/html/2507.11004v1, https://github.com/texttron/BrowseComp-Plus

### F11 · 2025-06 / 2025-08 · Benchmarks for conflicting sources (CONFLICTS, NATCONFQA)
- What: CONFLICTS (arXiv 2506.08500) is an expert-annotated taxonomy of conflict types with the desired behaviour for each; models often mishandle conflicts, and explicit prompting to reason about conflicts helps. NATCONFQA (2508.12355) grades multi-answer QA on finding *all* valid answers *and* flagging the conflicting pairs. Neither is history-specific.
- Track: testing
- Affects: the Caesar and Kangxi/Qianlong rubrics; the "sources disagree" note
- Magnitude: n/a (initial)
- Suggested response: adopt the NATCONFQA framing as rubric items: every valid answer named, the conflict pair stated, each side attributed. Point to CONFLICTS for a guard in the skill: classify the conflict (an outdated source, differing frames such as formal reign against actual power, genuine scholarly dispute) before writing the note. The Qianlong case is a frame conflict, not a factual one.
- Sources: https://arxiv.org/abs/2506.08500, https://arxiv.org/abs/2508.12355v1

### F12 · 2024-2025 · ALCE citation recall and precision are the standard definitions
- What: Citation recall asks whether the concatenated citations of a statement entail it. Citation precision flags a citation as irrelevant if it does not entail the statement alone *and* removing it leaves the rest still entailing it. The NLI judge (TRUE, T5-11B) agreed with humans 85.1% (recall) and 77.6% (precision) of the time and misses partial support; later work moves to atomic claims.
- Track: testing
- Affects: the outcome cases (citation quality)
- Magnitude: n/a (initial)
- Suggested response: adopt the definitions in TESTS.md and the llm-grader rubric ("every dated claim has a citation that supports it alone"). The deterministic part is the quote-span check (F5).
- Sources: https://arxiv.org/pdf/2305.14627, https://arxiv.org/pdf/2409.08014

### F13 · current docs · Framework assertion types that fit
- What: promptfoo `factuality` (OpenAI-evals categories A–E against a reference; D, disagreement, fails; tunable), `model-graded-closedqa` (single criterion), `llm-rubric`, and `search-rubric` (a judge with web search, for live facts). Inspect: `includes()`, `match(location=...)`, `model_graded_fact()`, `model_graded_qa()` (grader model selectable). DeepEval: `FaithfulnessMetric` (output against `retrieval_context`, with `penalize_ambiguous_claims`) and GEval. The agentskills.io evals.json is `{skill_name, evals:[{id, prompt, expected_output, files, assertions[]}]}`, with grading.json `assertion_results[{text, passed, evidence}]` and benchmark.json with/without-skill deltas. Its advice: use scripts for mechanical checks, and drop assertions that pass in both arms.
- Track: testing
- Affects: the evals.json format; the outcome graders
- Magnitude: n/a (initial)
- Suggested response: point. evergreen's evals.json already aligns. A factuality-style "subset/superset/disagree" check fits Kangxi; FaithfulnessMetric's idea (answer against the fetched pages) maps onto the sources.json quotes. Avoid search-rubric in the suite: a live-search judge would also be answering from search, which muddies the baseline.
- Sources: https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/factuality/, https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/search-rubric/, https://inspect.aisi.org.uk/standard-scorers.html, https://www.deepeval.com/docs/metrics-faithfulness, https://agentskills.io/skill-creation/evaluating-skills

### F14 · current docs · Wikidata date semantics hw.py must encode and test
- What: Precision codes: 6 millennium, 7 century, 8 decade, 9 year, 10 month, 11 day (higher codes are legacy). Calendars: Q1985727 proleptic Gregorian, Q1985786 proleptic Julian. The UI defaults to Julian before 1583. **JSON has no year 0 (-0001 = 1 BC), but RDF/SPARQL uses XSD year 0 (1 BC = 0000) and converts BCE values to Gregorian** (8 BC 27 Nov appears as -0007-11-25). Year-precision dates stored as 1 January are conversion artefacts. Only UTC is supported.
- Track: testing
- Affects: hw.py dates; entities.json; unit tests for hw.py
- Magnitude: n/a (initial)
- Suggested response: adopt. hw.py unit tests (deterministic, no model): JSON `-0100` maps to "100 BC" and to EDTF `-0099`; SPARQL `-0099` maps back to "100 BC"; precision 9 never renders a day; claim precision ≤ source precision (a day claim backed only by month-precision sources fails, as with Caesar's preferred statement, F1); the calendar model is carried into entities.json. Python's `datetime` starts at year 1 (proleptic Gregorian), so do Julian↔Gregorian conversion with Julian Day Number arithmetic. Test vectors: JDN 2299160 = 4 Oct 1582 Julian, 2299161 = 15 Oct 1582 Gregorian.
- Sources: https://www.wikidata.org/wiki/Help:Dates, https://en.wikipedia.org/wiki/Conversion_between_Julian_and_Gregorian_calendars

### F15 · RFC 7946 and EDTF · minimal stdlib validator checklist for packs
- What: GeoJSON: `type` in the nine case-sensitive types. Feature has `geometry` (object or null) and `properties` (object or null); `id` is a string or number. A position has ≥2 numbers, `[lon, lat]`, so lon in [-180, 180] and lat in [-90, 90]. A LineString has ≥2 positions. A Polygon ring has ≥4 positions with first equal to last (winding is SHOULD: warn, never reject). `bbox` has length 2n. `crs` is obsolete: warn. Members must not cross types. More than ~6 decimals: warn. EDTF (LoC 2019; Level 0 is mandatory): extended format only; L1 adds `?`, `~`, `%` at the end, `X` digits, `..` for open interval ends, negative years, `Y` long years and seasons 21–24. EDTF follows ISO 8601 astronomical numbering (0000 = 1 BC), which conflicts with Wikidata JSON. That rests on ISO 8601 secondary sources; the LoC page itself gives no BCE example.
- Track: testing
- Affects: the pack action case; `hw.py validate-pack`
- Magnitude: n/a (initial)
- Suggested response: adopt. `hw.py validate-pack <dir>` checks: the files exist; every JSON parses; each entities.json entity has `qid` matching `^Q\d+$`, a date with `precision` (int 0–11), `calendar` (a QID) and an optional `edtf` that matches an L0/L1 regex; places.geojson passes the checks above plus a heuristic swapped-coordinate warning (Rome near [12.5, 41.9]; [41.9, 12.5] flags); timeline.json is sorted by astronomical year; the references/ manifest has licence, url, date and place per file; sources.json has url, retrieved, quote and tier. Eval: `{type: command, run: "python hw.py validate-pack out/pack", expect: "exit 0"}`, plus a negative fixture pack (lat/lon swapped, an open ring, `wdt`-only dates) that must fail.
- Sources: https://www.rfc-editor.org/rfc/rfc7946, https://www.loc.gov/standards/datetime/, https://en.wikipedia.org/wiki/0_AD

### F16 · standing · Independence rule: circular reporting
- What: Wikipedia's own guidance: do not cite Wikipedia, check its references, and suspect any later "reliable" source that may have copied the article. Its circular-reporting template says to find when the fact entered the article (the Blame tool) and seek a source published earlier. Example: the Alan MacMasters toaster hoax lasted over a decade.
- Track: testing
- Affects: the corroboration rule; a case in evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt. In sources.json, each source carries `derived_from` (for example "wikipedia", or "wikidata→bbc"). Two sources count as independent only if neither is Wikipedia/Wikidata/DBpedia or a mirror, and they do not share a `derived_from`. Wikidata counts as the claim-holder, and the reference it cites is the source. At least one source is tier primary or scholarly (OpenAlex/Crossref DOI, a primary text, an official site). Eval: a regex on sources.json requires two distinct non-wiki hosts per dated claim; decoy fixture: a question whose only online support is wiki mirrors must produce "unverified".
- Sources: https://en.wikipedia.org/wiki/Circular_reporting

### F17 · baseline knowledge · No calendar or dispute benchmark for history; HiST-LLM is the history baseline
- What: HiST-LLM (NeurIPS 2024, Seshat; 36k data points, four-choice) found 33.6 to 46% balanced accuracy, weakest for Oceania and Sub-Saharan Africa. Test of Time (ICLR 2025) is synthetic temporal reasoning. No LLM benchmark of Julian/Gregorian, BCE or disputed-date handling was found; ChronoSense and TimeQA did not surface. The quiet result: the date-handling cases have to be built here.
- Track: testing
- Affects: the baseline case; adding a regional case
- Magnitude: n/a (initial)
- Suggested response: adopt one non-Western outcome case (HiST-LLM's weak regions), for example an Ethiopian or Mali ruler's reign, gold re-verified from sources. Add a calendar case: "On what date did the Battle of Hastings / Russia's October Revolution happen?", expecting both the Old Style and New Style date for 1917. Note HiST-LLM as the published baseline.
- Sources: https://proceedings.neurips.cc/paper_files/paper/2024/file/38cc5cba8e513547b96bc326e25610dc-Paper-Datasets_and_Benchmarks_Track.pdf, https://research.google/pubs/test-of-time-benchmarking-llms-on-temporal-reasoning/

## Overall magnitude: n/a (initial)

## Open questions:
- Resolved: the Caesar gold. Wikidata itself records 12/13 July 100 BC (preferred, month precision, disputed) and 102 BC (disputed, JSTOR); the gold holds.
- Resolved: the Microsoft gold is 4 April 1975 (Wikidata, official MS source).
- Open: the Kangxi/Qianlong gold dates were not re-verified in this pass (subject track).
- Open: urlhealth's repository is unknown, perhaps unreleased.
- Open: the exact CONFLICTS taxonomy labels (full paper not read).
- Open: whether the EDTF spec text itself states year 0 = 1 BC (only ISO 8601 secondaries were seen).
- New: should the Microsoft rubric accept a 1981 incorporation mention? The incorporation date is unverified.
- New: hw.py needs an `HW_HOME` override so eval runs can grade the cache inside the workspace.

## Search plan notes:
- Worked: Wikidata `wbgetclaims` API (fast primary gold, retrieval-dated); the code.claude.com plugin-evals page (it has mock MCP servers, unknown to the caller's plan); the arXiv HTML of the 2026 citation papers; agentskills.io for the evals.json schema.
- Noise: themoonlight/alphaxiv/catalyzex mirrors; benchlm (mixes SimpleQA with Verified); skills.sh "research" skills (no evals); Microsoft secondary trivia sites.
- Better sources: Wikidata API for gold; Kaggle FACTS and SimpleQA Verified for leaderboards.
- The web search budget (shared limit) ran out on query 28 (inspect_evals implementations unchecked).

## Tracks covered: subject: 0 queries · tooling: 0 · practice: 0 · testing: 27 (+1 refused by budget)

## Upcoming events: none found (Kaggle SimpleQA Verified and FACTS leaderboards update continuously)

## Nothing changed: no (creation pass)

## Cost: searches 28 (1 refused by budget) · fetches 16 · tool calls 51
