# Method: how historians and reference librarians answer

Back to [SKILL.md](../SKILL.md). Each rule cites the finding behind it in [RESEARCH.md](../../../RESEARCH.md).

## The reference interview (RUSA guidelines; R-20261017-11)

A short interview before searching, done in your head unless the readings truly diverge:

| Ambiguity | Readings | Example |
|---|---|---|
| Rule | formal reign, de facto power, regency | Kangxi reigned 61 years, ruled for by regents at first; Qianlong abdicated in 1796 and held power to 1799 |
| Founding | idea, partnership, incorporation, trade-name registration, first product | Microsoft: partnership 4 April 1975, trade name 1976, incorporated 25 June 1981 |
| Calendar | Julian, Gregorian, Old Style with a 25 March year start, lunisolar era dates | George Washington: born 11 February 1731/32 O.S. (the year then began on 25 March), 22 February 1732 N.S. |
| Superlatives | whose list, which dynasties count, what unit | the longest-ruling emperor depends on whether Nanyue's Zhao Tuo counts |
| Names | the same name for different people or places | several Alexandrias; two Han eras named 建武 |

State the reading in the answer's first line. Offer the other reading in a sentence. End with an offer to go
further only when a follow-up would change the answer.

## Reading a source (Historical Thinking Chart, Wineburg; R-20261017-11)

- **Sourcing**: who wrote it, when, how close to the event, why. Suetonius wrote about 150 years after Caesar's
  birth; a 1995 Fortune interview with the founders is close to Microsoft's founding.
- **Contextualisation**: what the author could know; what genre the text is (a law quoted by Macrobius, a
  biography, a press release, a filing under penalty of law).
- **Corroboration**: does an independent source agree, and does it derive from the first?
- **Close reading**: what the passage actually says; an inference ("he was 56 when he died") is not a date.

Primary or secondary depends on the question: a 2025 anniversary post is primary for what Microsoft says about
itself and secondary for 1975.

## Source hierarchy

Tertiary sources (Wikipedia, Britannica, encyclopedias, AI answers) route you and lend you their citations;
cite what they cite, after reading it. Curated structured data (Wikidata with references, Pleiades, PeriodO,
DPRR, CBDB) sits between: cite the statement's own reference. Primary sources and peer-reviewed scholarship
carry the answer. A Wikidata statement with no reference beyond "imported from Wikimedia project" is a lead.

## Independence (R-20261017-17)

Two sources agree independently only when neither copies the other and neither copies Wikipedia. Citogenesis is
documented: a false Wikipedia claim reached newspapers and books, which Wikipedia then cited back (the toaster
"inventor" Alan MacMasters, 2012-2022). Prefer a source that predates the claim's first appearance on Wikipedia.
Record `derived_from` when one source cites another; `hw.py verify sources` counts only independent ones.

## Disagreement (R-20261017-24)

Classify before writing the "Sources disagree" note:

- **Outdated source**: a later find or edition corrected it. Give the current view and say the older one is
  superseded.
- **Different frame**: both are right about different things (formal against de facto reign; founding against
  incorporation; Julian against Gregorian). Give both with their frames.
- **Genuine scholarly dispute**: name each position's holders and evidence, and say which is the consensus
  (due weight, no false balance). Caesar's birth year: Mommsen argued 102 BC from the minimum ages for offices;
  Badian (1959) and most since hold 100 BC, which every ancient source implies.

## Contested and national narratives (R-20261017-19)

The language of the prompt shifts how a model frames a contested event. For borders, wars, genocides,
colonial history and national founding stories: search in the language of each party, cite sources from more
than one country, attribute each account ("Turkish historiography holds ..., Greek accounts ..."), and state
settled findings as fact (Council of Europe multiperspectivity; Wikipedia's due weight).

## Where memory is weakest

HiST-LLM (Seshat, NeurIPS 2024): the best model scored 46% on four-choice history questions, worst for
Sub-Saharan Africa, Oceania and recent periods. The national archives of India, much of Africa and Latin America
are browse-only, so answers there rest on scholarship (OpenAlex), Wikidata references and scanned books
(Internet Archive). Say so in the confidence line.

## Stopping early (R-20261017-21)

Agents stop before the task is complete and do not say so. Before answering, check: every part of the question
answered or marked unanswered; every count computed in code; every source in the list read in this run.
