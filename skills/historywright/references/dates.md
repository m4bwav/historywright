# Dates: the traps, and the hw.py command for each

Back to [SKILL.md](../SKILL.md). Sources: R-20261017-2, -9, -10 in [RESEARCH.md](../../../RESEARCH.md).

| Trap | What goes wrong | Do this |
|---|---|---|
| No year 0 | 100 BC to AD 100 is 199 years, not 200 | `hw.py cal span "100 BC" "AD 100"` |
| Astronomical years | ISO and EDTF write 100 BC as `-0099` | `hw.py cal date -0099-07-12` reads it back |
| Wikidata JSON vs SPARQL | JSON `-0100` is 100 BC; SPARQL prints `-0099-07-11` (year 0, converted to Gregorian) | read statements with `hw.py wd claims`, never `wdt:` alone |
| Precision | a value at year precision is written as 1 January | the `precision` field; `flags` warns on 1 January |
| Roman dates before 45 BC | the republican calendar drifted months from the sun | say "republican calendar"; the Julian reading is proleptic |
| Julian vs Gregorian | countries switched between 1582 and 1923 | `hw.py cal date "<date>" --country GB` (or RU, SE, FR, GR, ...) |
| Old Style year start | in Britain before 1752 the year began on 25 March, so "11 February 1731" then is 1732 in January-start years | hw.py reads years as starting 1 January: pass 1732; `--country GB` prints the dual year as written then (1731/32) |
| Old Style / New Style | 25 October 1917 O.S. is 7 November N.S. | `hw.py cal date "1917-10-25 O.S." --country RU` |
| Proleptic Gregorian | some databases store ancient dates as Gregorian | `wd claims` flags it and gives the Julian reading |
| AUC | ab urbe condita (Varronian): AUC 1 = 753 BC, AUC 654 = 100 BC | `hw.py cal date "AUC 654"` |
| Islamic | tabular before 1924; observed months can differ by a day or two | `hw.py cal date "AH 1300"`; say "tabular" |
| East Asian eras | one name can belong to several eras in different dynasties and countries | `hw.py cal era 建武`, `hw.py cal cjk 康熙六十一年十二月二十九日` |
| Era name vs reign | an era name often starts the year after accession and outlasts the death by months | give accession and death dates, not the era span, for a reign |
| Ages and reign lengths | memory rounds and miscounts | `hw.py cal span <start> <end>`; years, months, days and total days |

East Asian conversions read the DILA Time Authority Database (Dharma Drum Institute of Liberal Arts,
CC BY-SA 3.0), built into `~/.historywright/dila_time.sqlite` on first use (`hw.py cal setup`). Coverage:
China about 220 BCE-1912, Japan 593-1872, Korea 56 BCE-1885. Credit DILA in any answer that uses it. Academia
Sinica's two-thousand-year converter (兩千年中西曆轉換) is the cross-check.

EDTF (levels 0 and 1; a disputed date as a level 2 set) is the machine form in packs: `1975-04-04`,
`-0099-07`, `-0099-07~` (circa), `-0099-07-12?` (uncertain), `1661/1722` (interval), `[-0099-07-12,-0099-07-13]`
(one of). A disputed date is a set or a range, never a point.
