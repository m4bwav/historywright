# Kickoff: build historywright (Step 2), an evergreen historical-research plugin

Written 2026-10-17, after Step 1 and Mark's answers to its forks. Paste this into a fresh session started in the folder that holds this repository.

## The goal

Build `historywright`, a public evergreen plugin that answers history questions by researching sources, not by reciting what the model remembers. Examples: "When was Caesar born?", "Who was the longest-ruling emperor in Chinese history?", "When did Bill Gates found Microsoft, and with whom?" Each answer has inline citations, a confidence line that says what is uncertain and why, and a "sources disagree" note. The plugin's knowledge base is about **how to find historical answers**: sources by era, region and kind of question; query recipes; reliability and access notes; cached answers with sources and retrieval dates. Model knowledge routes questions and sanity-checks results, and is never the answer. Research packs feed polywright (3D) and cinewright and comfyui-gen (video).

## Where things stand

Step 1, the evergreen creation pass, is done (2026-10-17): seven parallel research passes covering subject, tooling, practice and testing. Mark has answered the three forks. Nothing is built yet. There is no repo and no git.

Mark's keys are live and tested (2026-10-17): the OpenAlex key ($1 a day) and the World Historical Gazetteer token are in `~/.historywright/config.json` under `keys.openalex.api_key` and `keys.whg.token`. Read them from there and never copy them anywhere else. The repo's `.gitignore` and CI should both guard against leaks: CI fails on any 40-plus-character token-like string outside test fixtures. Mark asked that the token stay out of the repo.

## Read first

1. `historywright/ai-docs/HANDOFF.md`, then `ai-docs/research/2026-10-17-creation-pass.md`. §7 of the synthesis is the proposed layout, §8 the forks, §5 the practice guards and §6 the testing plan.
2. `historywright/RESEARCH.md`: Current understanding, Open questions, and R-20261017-1 to -24. Every guard in the skill text cites its `R-` entry.
3. `ai-docs/decisions/2026-10-17-step1-rulings.md` (nine rulings) and `ai-docs/decisions/2026-10-17-forks-mark.md` (Mark's answers).
4. `ai-docs/notes/api-keys-setup.md`: every optional key and how to get it. This becomes the README's "Optional keys" section and the spec for `hw.py keys`.
5. Check that the installed evergreen is 0.17.0 or later (`claude plugin list`). Read the evergreen-new skill (Steps 3 to 5) and PROTOCOL §8 and §11.
6. Mark's rules in the vault user PROFILE (`<vault>/user/PROFILE.md`, section "Code and repos"; `everlast.py vault where` prints the vault).
7. Patterns to copy (README and HANDOFF of each):
   - `Ai/polywright`: a hub skill with siblings, a stdlib CLI, and the asset contract in `skills/polywright/references/contract.md`.
   - `Ai/everscout`: user data in `~/.<tool>/`, seed data in the repo.
   - `Ai/readwright`, `Ai/fetchwright`, `Ai/chartwright`.
   - Prior art to read before writing hw.py:
     - kltng/humanities-skills: `cjk-calendar`, `wikidata-search` and their `evals/evals.json`;
     - fuzheado/wikipedia-ai-skills: `wikimedia-api-access` and `wikidata-reconciliation`.

## The forks (settled 2026-10-17)

1. **Keys: optional and free, automated where possible.** Everything works keyless. hw.py reads keys from `~/.historywright/config.json`, with environment variables (`OPENALEX_API_KEY`, `WHG_TOKEN`, `HW_CONTACT`) taking precedence. `hw.py keys` gives every user the route the notes describe:
   - `keys openalex --email ADDR` posts the documented API request, but only after the user has given their address and said yes;
   - `keys whg` opens the ORCID sign-in page with a per-OS branch and saves the token the user pastes;
   - `keys status` checks each key.
2. **East Asian eras.** On first use, `hw.py cal` downloads DILA's own `authority_time.2012-02.zip` (1.34 MB; from authority.dila.edu.tw or github.com/DILA-edu/Authority-Databases) and builds the SQLite table in `~/.historywright/`.
   - Licence: CC BY-SA 3.0, so attribute DILA in answers and in the README.
   - Do not fetch kltng's prebuilt `calendar.db`; its repository has no licence.
   - Follow kltng's design and credit it.
3. **Paid sources: none.** Gated sources are link-out only.

## Step 2: design and build

Build to §7 of the synthesis unless the build shows a better shape; record any change in `ai-docs/decisions/`.

- **`historywright` (hub)**:
  - Intake: a short reference interview that states which reading of the question is answered.
  - Route with the era outline.
  - Wikidata full statements and place sources first, then follow references to scholarship and primary texts.
  - Corroborate with two independent sources (no Wikipedia mirrors, no shared `derived_from`), one of them primary or scholarly.
  - Dates in hw.py; cite only what the run fetched and read.
  - Write the answer, the confidence line and the classified "sources disagree" note, then the cache entry.
  - "Unverified" when sources cannot be reached.
- **`historywright-sources`**: the source registry (seeded from the four subject reports, about 60 sources with route, licence, access, tier and per-host pace), the era outline (from the routing articles and PeriodO; within the size budget), query recipes, and `hw.py probe` at every refresh.
- **`historywright-pack`**: `answer.md`, `sources.json` (with supporting quotes), `entities.json` (QIDs, the EDTF date object of synthesis §2), `places.geojson`, `timeline.json` (source sentence and range per row), and `references/`. References are CC0-first museum records with licence, URL, date, place and accession number, plus a per-period anachronism checklist. The layout matches polywright's asset contract.
- **`hw.py`** (stdlib): `wd`, `wp`, `place`, `oa`, `doi`, `cal`, `cache`, `verify` (quote span, URL health, DOI, QID), `validate-pack`, `probe`, `keys` and `lint`. One shared HTTP layer: a contact User-Agent, per-host throttles, concurrency 3, Retry-After. `HW_HOME` overrides `~/.historywright` for evals.
- **End-to-end example**: research a Roman legionary of 50 BC, export the pack, have polywright read its references, and record the result. Expect CC0 museum APIs to return Greek and Etruscan helmets. Late-Republican kit comes from Commons and Europeana with per-file licences.

## Tests (evergreen-test)

Use the corrected gold in RESEARCH.md R-20261017-12:

- **Outcome, Caesar**: "12 or 13 July 100 BC", with 12 July from Macrobius and 13 July from a disputed reading of Dio, Mommsen's 102 BC argument noted, and two sources. It fails on "99 BC" or "11 July".
- **Outcome, Kangxi**: 61 years, 1661–1722, plus Qianlong's abdication in 1796 and de facto rule to 1799.
- **Outcome, Microsoft**: Gates and Allen, 4 April 1975, Albuquerque; do not require an official page that names the day.
- **Action cases**:
  - the trace shows `wbgetclaims` or `psv:` before the answer, not a lone `wdt:`;
  - a cache entry with sources and a retrieval date;
  - a pack that passes `validate-pack`, and a negative fixture pack that fails.
- **Cases the research adds**:
  - October Revolution O.S./N.S.;
  - a non-Western reign;
  - "five key books on X" checked in a catalogue;
  - a planted misattributed quote;
  - a question with only Wikipedia-mirror support (it must come back unverified).
- **Decoys**:
  - "write a story set in ancient Rome";
  - "summarise this history PDF" (that is readwright's job);
  - "what happened in today's news".
- **Baseline without the skill**: the worth check must show the skill beats memory; expect the disputed-date and reign cases to show it.
- **Harness**: `claude plugin eval`, with fixture mocks of the Wikidata JSON for the Caesar case. Bash needs WSL2 on Windows, otherwise use `EG worth --ab`.

## Launch set (PROTOCOL §8 and Mark's PROFILE)

- Public repo `m4bwav/historywright`.
- README with a hero banner (comfyui-gen, 1536x640, four seeds, a contact sheet, `.github/images/banner.jpg`).
- Install and quick-start sections, LICENSE, the tiered SECURITY.md with private vulnerability reporting on, CI, AGENTS.md plus a CLAUDE.md whose first line is `@AGENTS.md`, and the description and topics.
- An ai-docs doc set via everlast-setup. The current `ai-docs/` files (log, HANDOFF, decisions, research, this prompt) carry over into it.
- A GitHub wiki via wikiwright. The first page must be saved in the web interface, and that click is Mark's: ask him.
- Registered in the evergreen catalog (`evergreen.py init`, which keeps the existing RESEARCH.md) and installed through the mark-local marketplace.

## Rules

- Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`. No AI attribution anywhere.
- Merge your own PRs once checks pass. Tagging a release and directory submissions wait for Mark's go-ahead.
- Parallel researchers share about 200 WebSearch calls a turn. If you run several, cap each one (about 25) and prefer direct API fetches.
- Never index or walk AppData. Kill processes only by PID.

## When to stop and ask

- Before signing up for or paying for any source, and before installing a large dependency.
- Before the first release tag.
- Before requesting a key for anyone. Mark's keys are already handled.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
