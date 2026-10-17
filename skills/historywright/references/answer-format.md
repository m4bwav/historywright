# Answer format and worked examples

Back to [SKILL.md](../SKILL.md). The examples show the shape only. They are not sources: a run fetches and reads
its own sources every time, and these facts may be refined by later scholarship (gold answers checked
2026-10-17, R-20261017-12).

## Shape

```
<reading answered>. <answer with inline citations>.
<alternatives, the other reading, who holds each view>

Confidence: <high|medium|low>: <what is uncertain and why>
Sources disagree (<outdated source | different frame | scholarly dispute>): <who says what>
Sources:
[1] <author>, <title>, <locator>. <URL> (read YYYY-MM-DD)
[2] ...
AI-researched with historywright; sources fetched and read on YYYY-MM-DD.
```

- Inline citations sit next to the claim they support, not at the end of the paragraph.
- The confidence line names the uncertainty: a disputed reading, one source only, a proleptic date, a region with
  thin coverage. "High" needs two independent sources that agree, one of them primary or scholarly.
- "Sources agree." is a valid note. Leave neither out.
- Dates: give the calendar when it matters ("25 October 1917 (Old Style; 7 November New Style)"), and say
  "republican calendar" for Roman dates before 45 BC.

## Caesar's birth (a genuine dispute and a calendar trap)

Wikidata holds four statements for Q1048 P569. The preferred one is July 100 BC at month precision, flagged
disputed, with earliest 12 and latest 13 July; another is 102 BC, also flagged. A truthy `wdt:P569` read shows
only the first; a naive SPARQL read prints `-0099-07-11` (XSD year 0, converted to Gregorian).

> Julius Caesar was born on 12 or 13 July 100 BC [1][2]. 12 July is the date of his official festival under
> the law quoted by Macrobius (Saturnalia 1.12.34) [1]; 13 July rests on a disputed reading of Cassius Dio
> 47.18 [2]. Every ancient source implies 100 BC [3]; Mommsen argued for 102 BC from the minimum ages for
> Caesar's offices, a view Badian rejected in 1959 and most historians now reject [4].
>
> Confidence: high for 100 BC; medium for the day: the sources give two days, and these are Roman
> republican-calendar dates with no exact solar equivalent.
> Sources disagree (scholarly dispute): 12 July (Macrobius) against 13 July (Dio, disputed reading); 102 BC
> (Mommsen) against 100 BC (Badian, consensus).

Wrong answers the tests catch: "11 July" (the SPARQL artefact), "99 BC" (year 0 confusion), a single day stated
as certain.

## The longest-reigning Chinese emperor (a frame question)

> By formal reign, the Kangxi Emperor: 61 years, 1661-1722 (his era name ran 1662-1722), with regents ruling
> for him at first [1][2]. His grandson Qianlong reigned about 60 years (acceded 1735), abdicated on
> 9 February 1796 so as not to outlast Kangxi, and kept power as Retired Emperor until he died on
> 7 February 1799, the longest de facto rule at about 63 years [3].
>
> Confidence: high: the reign dates are undisputed; "longest" depends on counting formal reign or power.
> Sources disagree (different frame): formal reign (Kangxi) against actual power (Qianlong).

`hw.py cal span` computes both lengths; `hw.py cal era 康熙` gives the era's own first and last days.

## Microsoft's founding (founding against incorporation)

> Bill Gates and Paul Allen founded Microsoft (styled Micro-Soft) as a partnership on 4 April 1975 in
> Albuquerque, New Mexico [1][2]. It moved to the Seattle area (Bellevue) on 1 January 1979 and was incorporated
> in Washington on 25 June 1981 [3].
>
> Confidence: high for the founders, place and year; medium-high for the day: Microsoft's own pages give 1975
> and the 1981 incorporation but not 4 April, which comes from contemporary accounts and the founders' memoirs.
> Sources agree.

Do not demand an official page that prints the day; none does.

## Unverified

> Unverified: the only pages giving this date are Wikipedia and sites that copy it, and its footnote leads to a
> dead page with no archived copy. What would settle it: <the record, archive or book to check>.
