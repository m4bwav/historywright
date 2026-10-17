# historywright handoff

Updated 2026-10-17 (end of Step 1 session).

## State

- Step 1, the creation pass, is done. Mark has answered the three forks ([decisions/2026-10-17-forks-mark.md](decisions/2026-10-17-forks-mark.md)), so Step 2 (design and build) is ready to start from [next-session-prompt.md](next-session-prompt.md).
- Nothing is built: no skills, no hw.py, no repo, no git. The folder holds research, decisions and notes.
- Keys: the OpenAlex key and the WHG token are both live and tested (2026-10-17). Both are in `~/.historywright/config.json`, restricted to Mark's account. They must never be committed.

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. [research/2026-10-17-creation-pass.md](research/2026-10-17-creation-pass.md): §7 is the layout, §5 the guards, §6 the tests.
3. [../RESEARCH.md](../RESEARCH.md): R-20261017-1 to -24, plus the Open questions.
4. [decisions/](decisions/): the Step 1 rulings and Mark's forks.
5. [notes/api-keys-setup.md](notes/api-keys-setup.md): the key process, which becomes the README section and `hw.py keys`.
6. [log.md](log.md).

## Key facts a builder needs

- Wikidata: read full statements (`wbgetclaims` or `psv:`), never `wdt:` alone. JSON uses historical BCE numbering and SPARQL uses XSD year 0.
- Wikimedia allows 10 requests a minute without a contact User-Agent and 200 with one.
- OpenAlex: a key is needed past page 1. Met: use v1.1 search. ctext is paid. Chronicling America is reachable only through loc.gov.
- DILA time data is CC BY-SA 3.0. Build the table locally from DILA's 1.34 MB zip, not from kltng's unlicensed db.
- Caesar gold: "12 or 13 July 100 BC". Kangxi gold: also covers Qianlong's de facto rule to 1799.

## Open

- RESEARCH.md Open questions: WHG v3 docs, the Wikipedia references route, the Seshat licence, whether bot-wall 403s clear with an honest User-Agent, and more.
- Evergreen learning to file at wrap-up: parallel researchers share about 200 WebSearch calls a turn, so cap each pass.
- Evergreen's session-start audit listed 8 units due for refresh (not run this session).
