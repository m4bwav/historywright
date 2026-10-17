# Creation pass 2026-10-17: subject-d-method-gold-answers (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-10-17 (live query) · Wikidata returns Caesar's birth in four forms, and a naive read of the SPARQL output gives "11 July 99 BC"
- What: `wbgetclaims` on Q1048, property P569, returns four claims. (1) Preferred: July 100 BC, month precision, Julian calendar (Q1985786), with qualifiers P1319 (earliest date) 12 July and P1326 (latest date) 13 July, P1480 sourcing circumstances Q18912752, and refs BBC History plus two books. (2) 13 July 100 BC, day precision, Julian, cited to two Google Books pages. (3) 102 BC, year precision, cited to JSTOR 295588 (a JRS article) and also flagged with P1480. (4) 100 BC, Gregorian model, cited to RE (1957). The same data over SPARQL (`wikibase:timeValue`) comes back as `-0099-07-11`: astronomical year numbering (1 BC = 0000), converted to proleptic Gregorian, so the Julian date shifts by 2 days. The JSON API uses historical numbering (`-0100` = 100 BC). This matches the documented rules: Wikibase DataModel says the timestamp uses historical numbering ("year 1 BCE is represented as -0001"), and the RDF format says the xsd:dateTime "represents the year 1 BCE as +0000". Precision codes: 9 year, 10 month, 11 day, 8 decade, 7 century, 6 millennium. Wikidata accepts nothing finer than 11.
- Track: testing (and subject)
- Affects: `hw.py` Wikidata query design; entities.json; the Caesar case in evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt. `hw.py` reads `psv:` full values with timePrecision and timeCalendarModel, keeps the JSON historical year, and never prints `wikibase:timeValue` or `wdt:` literals as dates. Read P1319/P1326/P1480 qualifiers as an uncertainty range. Add an eval case: the answer must not say "99 BC" or "11 July" for Caesar.
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1048&property=P569&format=json, https://www.mediawiki.org/wiki/Wikibase/DataModel, https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format

### F2 · 2026-10-17 · Gold answer verdict, Caesar: CORRECTED (day stays open, year 100 BC confirmed, attribution refined)
- What: Wikipedia now gives "12 or 13 July 100 BC". Its note cites Badian 2009 p.16 and says Macrobius Sat. 1.12.34 quotes Antony's law giving "the fourth day before the Ides of Quintilis" (12 July). It adds "Only Dio gives 13 July. All sources give the year 100 BC." The Dio reading is itself disputed. Dio 47.18.6 says the birthday feast was moved to "the previous day" because the Ludi Apollinares fell on it, and the Loeb editor's note on LacusCurtius reads the birthday as the 12th. Suetonius, Jul. 88, has "He died in the fifty-sixth year of his age", which implies 100 BC. Rolfe's Loeb note adds "The arguments in favour of 102 are however very strong." The 102 BC case goes back to Mommsen, based on the minimum ages for the curule offices (praetor in 62 BC, consul in 59 BC). Badian (JRS 1959) and Deutsch defend 100 BC, explaining the early offices by a dispensation or privilege. Current consensus is 100 BC.
- Corrected gold text: "Born 12 or 13 July 100 BC in Rome. 12 July comes from Macrobius (Sat. 1.12.34, quoting Antony's law) and was the official feast day. 13 July is inferred from Cassius Dio 47.18, whose reading is disputed. All ancient sources imply 100 BC (Suetonius, Jul. 88). Mommsen and others argued for 102 BC (some for 101) from the minimum ages for the offices of his career. The consensus is 100 BC. These are Roman republican calendar dates, before the Julian reform of 45 BC." Grader: accept 12 or 13 July if both are named or the dispute is flagged. Fail an answer that gives 102 BC as the fact, or a single day with no caveat.
- Track: testing
- Affects: Caesar case in evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://en.wikipedia.org/wiki/Julius_Caesar (note 5), https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Cassius_Dio/47*.html, https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html, https://resolve.cambridge.org/core/journals/journal-of-roman-studies/article/caesars-cursus-and-the-intervals-between-offices/08642B06B2D1F2916366780A2CF61FA0, https://resolve.cambridge.org/core/journals/journal-of-roman-studies/article/was-caesar-born-in-100-or-in-102-bc/BDE639D70E0F8A3A819F268D2E827975

### F3 · 2026-10-17 · Gold answer verdict, Chinese emperors: CORRECTED (add de facto power and the Zhao Tuo caveat; fix the dates)
- What: Kangxi reigned from 5 Feb 1661 (accession; the body text says enthroned 7 Feb) to his death on 20 Dec 1722, which Wikipedia gives as "61 years, 318 days". His era name ran 18 Feb 1662 to 4 Feb 1723, which is why museums write "Kangxi 1662–1722". Qianlong acceded on 18 Oct 1735, his era began 12 Feb 1736, he abdicated on 9 Feb 1796 "to allow his grandfather... to remain the longest-reigning Qing emperor at 61 years" (Wikipedia, citing the NYT), and he died on 7 Feb 1799. Academia Sinica's museum says that "instead of retiring... Qianlong maintained his grip on power" as Taishanghuang. Wikipedia's Kangxi article also says Qianlong had the longest period of de facto power, about 63 years. Kangxi ruled under regents for his first six or more years, so his effective rule was shorter than his formal reign. Zhao Tuo ruled Nanyue from 203 (or 204) to 137 BC, about 66 years. He called himself emperor from 185 BC and kept the title inside his kingdom after renouncing it toward Han in 180 BC. No source ranks him as the "longest-reigning Chinese emperor", but he is the obvious challenge if the question asks about "rulers". The Wanli figure (48 years) was not verified because the search budget ran out.
- Corrected gold text: "The Kangxi Emperor has the longest formal reign: 61 years (1661–1722; era name 1662–1722). His grandson Qianlong formally reigned about 60 years (acceded 1735, era 1736–1795). He abdicated on 9 Feb 1796 so as not to outlast Kangxi, but ruled as Taishang Huang until his death on 7 Feb 1799. That gives him the longest de facto hold on power, about 63 years. (Zhao Tuo of Nanyue ruled about 66 years, 203–137 BC, but is not counted among the emperors of the dynastic list.)" Grader: require Kangxi plus the Qianlong distinction. Give credit for mentioning the regency or the de facto point. Do not require Zhao Tuo.
- Track: testing
- Affects: longest-ruling emperor case in evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://en.wikipedia.org/wiki/Kangxi_Emperor, https://en.wikipedia.org/wiki/Qianlong_Emperor, https://museum.sinica.edu.tw/en/collection/17/item/146/, https://en.wikipedia.org/wiki/Zhao_Tuo, https://www.britishmuseum.org/collection/term/x117785

### F4 · 2026-10-17 · Gold answer verdict, Microsoft: CONFIRMED, with a sourcing caveat (no official page states the day)
- What: Microsoft's FY2002 10-K says "founded as a partnership in 1975 and incorporated in 1981" and "Mr. Gates co-founded Microsoft in 1975". Microsoft's facts page lists "1975 Microsoft founded", "June 25, 1981 Microsoft incorporates" and "Jan 1, 1979 moves from Albuquerque, New Mexico to Bellevue, Washington". Microsoft held its 50th anniversary on 4 April 2025, where Nadella said "Fifty years ago, Bill and Paul started Microsoft", and its Microsoft-50 page captions "1975: co-founders Bill Gates and Paul Allen". None of these official pages prints "April 4, 1975". That day is supported by the anniversary date and by secondary sources (Wikipedia, History.com). Wikipedia says the "Micro-Soft" name was Allen's and gives the New Mexico trade-name registration as 26 Nov 1976. The GatesNotes post and the memoir page returned 403, so they were not read.
- Gold text (kept, refined): "Bill Gates and Paul Allen founded Microsoft (first styled Micro-Soft) as a partnership on 4 April 1975 in Albuquerque, New Mexico. It was incorporated in Washington on 25 June 1981 and moved to Bellevue on 1 Jan 1979." The case's "primary or official source" requirement is met by the 10-K or the Microsoft facts page for the year, and the anniversary post for the day. The grader should not demand an official source naming 4 April.
- Track: testing
- Affects: Microsoft case in evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt (add the partnership versus incorporation distinction as a credit point)
- Sources: https://www.sec.gov/Archives/edgar/data/0000789019/000103221002001351/d10k.htm, https://news.microsoft.com/facts-about-microsoft/, https://blogs.microsoft.com/blog/2025/04/04/celebrating-microsofts-50-years/, https://news.microsoft.com/microsoft-50/, https://en.wikipedia.org/wiki/History_of_Microsoft

### F5 · 2026-09-21 · CJK Calendar Converter MCP server (kltng/calendar_converter): Chinese, Japanese, Korean and Vietnamese era dates through JDN
- What: An MIT-licensed MCP server with four tools: `convert_cjk_date`, `convert_gregorian_date`, `convert_jdn` and `search_era`. It uses the DILA Authority Database (CC BY-SA 3.0, attribution required) and cross-checks against CBDB and CeJS. Glama first saw it as v0.1.0 on 2026-09-21. Its own disclaimer says it is untested against all sources and may be wrong at dynastic transitions, on intercalary months, and off by one year at Vietnamese era boundaries. Install counts and the full repo were not read. Smaller alternatives for Japanese wareki: japan-utils-mcp (MIT, uvx) and seireki-mcp. The primary references to check against: Academia Sinica's "兩千年中西曆轉換" (listed on IHP's tools page) and DILA's time authority (authority.dila.edu.tw/time, frameset UI; no API documentation found).
- Track: tooling
- Affects: `hw.py` calendar conversion scope; the era-name step
- Magnitude: n/a (initial)
- Suggested response: point. Use its DILA-derived table, or the server itself, for era-name lookup instead of hand-writing tables. Keep Academia Sinica as the check. Read the repo in full in the tooling pass.
- Sources: https://glama.ai/mcp/servers/l8m0qo5u0c, https://github.com/kltng/calendar_converter, https://w9.ihp.sinica.edu.tw/leghist/pages/172

### F6 · 2026-02 · convertdate 2.4.1 (MIT): Julian, Islamic (tabular), Hebrew, Persian and others through JD; stdlib-only alternative
- What: convertdate 2.4.1 (February 2026 per a mirror) converts at noon of the day and covers Julian, Islamic, Hebrew and about 12 other calendars. It is a pip dependency, which conflicts with a stdlib CLI. Python's `datetime` covers only years 1–9999 of the proleptic Gregorian calendar. JDN = `date.toordinal() + 1721425` inside that range. Outside it, use integer formulas (Fliegel–Van Flandern 1968, per USNO). A check run here: Julian 12 July 100 BC (astronomical year −99) = JDN 1685091 = proleptic Gregorian −0099‑07‑10, which agrees with Wikidata's −0099‑07‑11 for 13 July.
- Track: tooling
- Affects: `hw.py` calendar subcommand
- Magnitude: n/a (initial)
- Suggested response: adopt the integer JDN algorithms in stdlib, with convertdate as the test oracle in evals. Islamic dates: treat them as tabular and label them as such. Umm al-Qura and observed dates were not researched because the search budget ran out.
- Sources: https://pypi.python.org/pypi/convertdate/, https://aa.usno.navy.mil/faq/JD_formula

### F7 · 2019-02-04 · EDTF (Library of Congress), the machine format for uncertain dates; it assumes Gregorian and astronomical years
- What: Level 0 is ISO 8601-1 dates and intervals. Level 1 adds negative years (`-0099`), `?` uncertain, `~` approximate, `%` both, `X` unspecified digits (`156X`), open or unknown interval ends (`../1985`, `1985/`), and `Y` long years. Level 2 adds per-component qualifiers (`2004-?06-11`), sets `[1667,1668]` (one of) and `{...}` (all of), `[..1760-12-03]` (on or before, i.e. a terminus ante quem), and significant digits (`1950S2`). Levels 1 and 2 correspond to ISO 8601-2:2019. Year numbering follows ISO, so `0000` = 1 BC and `-0099` = 100 BC. The spec has no calendar field. The python `edtf` package exists (PyPI).
- Track: subject
- Affects: entities.json schema; date normalisation step
- Magnitude: n/a (initial)
- Suggested response: adopt. Recommended entities.json date object: `{"as_written": "12 or 13 July 100 BC", "calendar": "roman-republican|julian|gregorian|chinese-lunisolar|islamic-tabular|...", "edtf": "[-0099-07-10,-0099-07-11]", "jdn": [1685091, 1685092], "precision": "day|month|year|decade|century", "wikidata_precision": 11, "qualifier": "disputed|circa|floruit|tpq|taq", "era_name": {"text": "乾隆元年", "system": "Qing"}, "sources": ["S1", "S2"]}`. EDTF and JDN are always computed in proleptic Gregorian with astronomical years. `as_written` and `calendar` keep the original. A disputed date is a set or range, never a single value. Floruit is `fl.` with an interval, circa is `~`, terminus post quem is an open interval `YYYY/..`.
- Sources: https://www.loc.gov/standards/datetime/, https://www.mediawiki.org/wiki/Wikibase/DataModel

### F8 · 1751/1752 · Julian to Gregorian adoption is per country and needs a table, not a constant
- What: The Calendar (New Style) Act 1750 (24 Geo II c.23) moved England's legal year start from 25 March to 1 January from 1752 and removed eleven days in September 1752 (2 Sep was followed by 14 Sep). Other cutovers: Catholic states 1582 (10 days), Sweden 1753 after its failed 1700–1712 scheme, Japan 1 Jan 1873 (1872 cut short), Russia 1918 (31 Jan followed by 14 Feb, 13 days), Greece 1923, Turkey 1926/27. China's date is given as 1912 or 1929 depending on the source. Dual dating ("1750/51", O.S./N.S.) is common in English sources for 1 Jan–24 Mar before 1752.
- Track: subject
- Affects: calendar step; `hw.py` adoption table
- Magnitude: n/a (initial)
- Suggested response: adopt. Ship an adoption table keyed by polity, sourced from the Wikipedia list and checked against statutes. Guard: when a date before the cutover in the place concerned comes from a local source, assume Old Style. Write O.S./N.S. when they differ. For English dates from 1 January to 24 March before 1752, show both years.
- Sources: https://www.legislation.gov.uk/apgb/Geo2/24/23/contents, https://en.wikipedia.org/wiki/List_of_adoption_dates_of_the_Gregorian_calendar_by_country, https://timeanddate.com/calendar/julian-gregorian-switch.html

### F9 · 2025-07-29 · AHA Guiding Principles for AI in History Education
- What: Approved by the AHA Council on 29 July 2025. Its relevant lines: "generative AI regularly hallucinates content, references, sources, and quotations", "any information provided by a generative AI tool could be false unless properly verified", "AI introduces a false sense of certainty where uncertainty exists" ("uncertainty is not a failure but a fundamental feature of historical inquiry"), and the material in "gated archives and nondigitized material is inaccessible to AI engines". It is written for teaching. A separate AHA committee covers research and publication; check for its output.
- Track: practice
- Affects: hub guards (never answer from memory; the confidence line; say what is undigitised)
- Magnitude: n/a (initial)
- Suggested response: adopt as the cited rationale for the "unverified" fallback and the confidence line. Add a guard: when the answer depends on undigitised archives, say so.
- Sources: https://www.historians.org/wp-content/uploads/2025/08/AHA-Artificial-Intelligence-in-History-Education.pdf, https://www.historians.org/news/aha-publishes-guiding-principles-for-artificial-intelligence-in-history-education/

### F10 · method · Historians' reading heuristics and the source hierarchy
- What: The Digital Inquiry Group (formerly SHEG) Historical Thinking Chart sets out sourcing, contextualization, corroboration and close reading, from Wineburg's think-aloud studies of historians. University history guides agree on three points. Whether a source is primary or secondary depends on the question. Tertiary sources (encyclopedias) are for orientation and are not to be cited as authority. Corroboration is the core test.
- Track: subject
- Affects: hub procedure order; the citation rule
- Magnitude: n/a (initial)
- Suggested response: adopt these steps. (1) Use tertiary sources (Wikipedia, Britannica) only to route and to collect citations. Follow their footnotes to a secondary or primary source and cite that. (2) For every cited source record who wrote it, when, how close they were to the event, and why they wrote it. (3) Corroborate with two independent sources that do not cite each other, as a guard against citogenesis. (4) Contextualize: name the calendar, the era, and the convention the source uses. Use Chicago notes-bibliography style for the full citation in answer.md. CMOS 18 (2024) was not verified this pass.
- Sources: https://www.inquirygroup.org/history-lessons/historical-thinking-chart, https://guides.uflib.ufl.edu/history/tertiarysources, https://guides.lib.montana.edu/historyresearch

### F11 · 2013 (revision pending since 2022) · RUSA reference behaviour guidelines
- What: The current approved text is the 2011 revision, approved by the RUSA Board on 28 May 2013. Its five areas are approachability, interest, listening/inquiring, searching and follow-up; the names are inferred, as the text was not fetched. A task force circulated a second draft in 2022 that adds disinformation evaluation. No adopted revision was found.
- Track: subject
- Affects: hub intake step
- Magnitude: n/a (initial)
- Suggested response: adopt a light "reference interview". Before searching, pin down what the question means: formal reign or actual power, founding or incorporation, which calendar. State the reading the answer chose, and end with a follow-up offer ("sources disagree, want the debate?").
- Sources: https://www.king.edu/wp-content/uploads/2018/09/PolicyReference_Services.pdf, https://connect.ala.org/acrl/discussion/the-rusa-behavioral-guidelines-task-force-needs-your-input-8

### F12 · method · Contested topics: due weight, no false balance, multiperspectivity
- What: Wikipedia's NPOV policy says to "avoid stating seriously contested assertions as facts" and to attribute them instead. It weights views by their share of reliable sources, rejects false balance, and says fringe views "should be clearly described as such". The Council of Europe (Stradling 2003; Quality history education principles, endorsed by the Committee of Ministers in June 2025) promotes multiperspectivity grounded in evidence. UNESCO's Pingel guidebook (2009) covers controversial textbook issues.
- Track: subject
- Affects: the "sources disagree" note; a guard for contested topics
- Magnitude: n/a (initial)
- Suggested response: adopt. The "sources disagree" note attributes each position to named scholars or institutions and says which holds the consensus. Settled findings, such as documented genocides, are stated as fact, and denial is described as denial. National narratives are presented as each side's position with sources from more than one country. Add a decoy or guard eval in which a denialist framing must not get equal weight.
- Sources: https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view, https://www.coe.int/en/web/observatory-history-teaching/-/decisions-visions-and-revisions-developing-historical-learning-about-multiperspectivity, https://efrec.gei.de/publications/detail/the-unesco-guidebook-on-textbook-research-and-textbook-revision

### F13 · method · Roman dates before 45 BC are republican-calendar dates (from model knowledge, unverified this pass)
- What: Caesar's "12 July 100 BC" is a date in the pre-reform Roman calendar, which drifted from the solar year before 46/45 BC. Wikidata tags it as Julian, and that conversion is nominal. AUC year to BC: BC = 754 − AUC (Varronian). Consular years go through Broughton's MRR and the Fasti.
- Track: subject
- Affects: calendar step; entities.json `calendar` value
- Magnitude: n/a (initial)
- Suggested response: adopt as a guard. For Roman dates before 45 BC, set `calendar: roman-republican` and do not claim a true solar-day equivalent. Verify the rule in the next pass.
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1048&property=P569&format=json (lead only)

## Overall magnitude: n/a (initial)

## Open questions:
- Resolved: Caesar's day and year (F2). The Kangxi/Qianlong framing (F3). The Microsoft date sources (F4). How Wikidata encodes BCE years and calendars (F1).
- New: Does the AHA research and publication committee have an AI statement? Are Wikidata's P1480 value Q18912752 and the JSTOR 295588 article what they appear to be? (Labels were not resolved.) Is kltng/calendar_converter used and accurate? (Read the repo.)
- Still open: Islamic AH conversion (tabular against Umm al-Qura or observed), Japanese nengō before 1873, the sexagenary cycle algorithm, the Wanli reign figure, regnal-year tables, the RUSA revision status, and the current CMOS edition. All are unsearched because the search budget ran out.

## Search plan notes:
- Subject: Wikipedia footnotes plus LacusCurtius (Thayer) gave primary passages quickly. Britannica (403) and GatesNotes (403) refuse fetching, so route them through fetchwright. SEC EDGAR 10-K full text works. Microsoft's own pages give the year and the incorporation date, not the day.
- Testing: live Wikidata `wbgetclaims` and SPARQL through WebFetch both work and are the best source of eval fixtures.
- Tooling: Glama lists the CJK MCP. The DILA site is a frameset with no API documentation. The registry and skills.sh were not queried (not this part's brief).
- Practice: the AHA PDF is readable through the Read tool after WebFetch saves it.
- Forums: not applicable. The vendor sources here are Wikidata (Phabricator, e.g. T99674 on the BCE offset) and the Wikimedia mailing lists. Add Phabricator to the plan.
- The search budget (200 per turn, shared across agents) ran out at query 28. The Islamic, nengō and Wanli queries failed.

## Tracks covered: subject: 18 queries · tooling: 4 · practice: 2 · testing: 4 (plus live Wikidata fixtures)

## Upcoming events: none found (the RUSA guideline revision has been pending since 2022, with no date)

## Nothing changed: no. This is a creation pass, and every finding is new.

## Cost: searches 28 (1 refused by the budget) · fetches 29 · tool calls 61
