# Era outline (routing only)

Back to [SKILL.md](../SKILL.md). Which sources to try first for a period and region. Spans are conventional and
approximate; scholars and regions draw them differently. Never cite this file: for a named authority's definition
of a period, use PeriodO (CC0), and cite the sources the route leads to. Registry ids in `code`.

## Any period

`wikidata` (statements and their references) · `wikipedia` (finder only) · `openalex`, `crossref` (scholarship) ·
`internet-archive`, `hathitrust` (scanned books) · `periodo` (period definitions) · `cliopatria` (polity borders
3400 BCE-2024) · `whg` (places worldwide, token) · `commons`, museum APIs (images for packs).

## Prehistory and early humans (before c. 3000 BCE)

Human evolution, the Palaeolithic, Neolithic and the first farmers. Go to scholarship (`openalex`) and museum
records first; Wikipedia's prehistory timelines route only (none is a good article). Radiocarbon dates are
calibrated ranges ("cal BP"); give the range and the calibration curve when a source names it.

## Ancient Near East and Egypt (c. 3500-332 BCE)

Mesopotamia, Egypt (Early Dynastic to Late Period), Hittites, Levant, Persia to Alexander. Chronologies differ
(high, middle, low for Mesopotamia; Egyptian dates carry decades of uncertainty before 664 BCE). `pleiades`,
`openalex`, museum records (`met`, `artic`, `british-museum` NC); cuneiform and papyri corpora are often
bot-walled (`papyri` link-out). Name the chronology used.

## Greece and Rome (c. 800 BCE-476 CE)

Archaic and Classical Greece, the Hellenistic kingdoms, the Roman Republic (509-27 BCE) and Empire.
`pleiades` (places), `dprr` (Republican people and offices), `perseus` and `lacuscurtius` (Greek and Latin texts
with translations), `fordham` (translated extracts), `openalex`; inscriptions via `edh` (bot-walled, link-out).
Dates before 45 BCE are republican-calendar dates. Consular years and Olympiads convert through scholarship.

## Late antiquity and Byzantium (c. 284-1453)

`pleiades` (to c. 640), `openalex`, `lacuscurtius`, `fordham`; Prosopography of the Later Roman Empire and the
Oxford Dictionary of Byzantium are print or gated (link-out).

## Medieval Europe (c. 500-1500)

`fordham` (Medieval Sourcebook), `avalon`, national libraries (`gallica` link-out, `europeana`), `openalex`,
`deutsche-biographie` for German lives. Julian calendar throughout; regnal years and saints' days need care.
Year starts varied (25 December, 1 January, 25 March): state the convention when a source gives one.

## Early modern Europe and the Atlantic world (c. 1450-1800)

`loc` (US and colonial records), `tna` (UK records), `avalon` (treaties, founding documents), `europeana`,
`internet-archive`. Julian to Gregorian switch by country (1582-1923): always `hw.py cal ... --country`.
British dates before 1752 may carry a 25 March year start (dual years).

## The Islamic world (622 onwards)

`openiti` (Arabic and Persian texts, bulk), `openalex`, `wikidata`; Encyclopaedia of Islam is gated (link-out).
Hijri dates before 1924 convert by the tabular calendar (a day or two off); say so.

## South Asia

Indus Valley (c. 3300-1300 BCE), Maurya (c. 322-185 BCE), then no single power until the Gupta: Shunga and Kanva
in the Ganges basin; Indo-Greek, Indo-Scythian (Azes), Indo-Parthian (Gondophares) and Kushan kings in the north-west;
the Northern Satraps at Mathura and the Western Satraps; the Satavahanas in the Deccan; Chera, Chola and Pandya in
the south. Inscriptions there are dated in eras whose start years scholars dispute (the Azes era: 58/57 or 47/46 BCE),
so compute each reading separately. Gupta (c. 320-550 CE), Delhi Sultanate (1206-1526),
Mughal (1526-1857), British rule (to 1947). National archives (`abhilekh-patal`) are browse-only: rely on
`openalex`, `wikidata` references, `internet-archive` scans, and name regional scholarship. Lower the default
confidence; dates for early dynasties carry wide ranges.

## China (c. 1600 BCE-1912, then the Republic and PRC)

Shang to Qing. Era names convert with `hw.py cal era|cjk` (DILA tables, c. 220 BCE-1912). Places: `chgis`
(221 BCE-1911, not redistributable). Officials and lives: `cbdb` (CC BY-NC-SA bulk). Texts: `kanripo`, `nlc`
(古籍 reader); `ctext` and `scripta-sinica` full tiers are paid (link-out). Formal reign and de facto power often
differ (regencies, retired emperors); era names start the year after accession.

## Japan and Korea

Japan: Asuka (538 or 552-710) to Edo (1603-1868) and Meiji; lunisolar dates before 1873 convert with
`hw.py cal cjk` (DILA, 593-1872). `ndl` and `japan-search` (no parallel calls). Korea: Three Kingdoms to Joseon
(1392-1897); DILA covers 56 BCE-1885. Name the country when an era name is shared.

## Southeast Asia

Funan, Angkor (c. 802-1431), Srivijaya, Majapahit, Dai Viet. Sparse open APIs: `openalex`, `wikidata`,
museum records, colonial archives through `europeana` and `tna`. Vietnamese era years can be off by one near
era boundaries in converted tables; check a second source.

## Sub-Saharan Africa

Aksum, Ghana, Mali (c. 1235-1600), Songhai, Great Zimbabwe, the Swahili coast, the Atlantic slave trade
(`slavevoyages` where listed), colonial and independence history. Memory is weakest here (HiST-LLM): lead with
scholarship (`openalex`), `eap` (Endangered Archives, browse), colonial archives (`tna`, `europeana`), and
oral-history caveats. Lower the default confidence and say why.

## The Americas before 1492

Olmec, Maya (Classic c. 250-900), Teotihuacan, Aztec (Mexica, 1428-1521), Andean cultures and the Inca
(c. 1438-1533), Mississippian. Maya Long Count dates convert through scholarship (GMT correlation; name it).
`openalex`, museum records (`met`, `smithsonian`, `artic`), `loc` for later codices and maps.

## Colonial and modern Americas

`loc` (newspapers through loc.gov, 20 requests a minute), `pares` (Spanish archives, browse), `hemeroteca-
brasileira` (browse), `federal-register`, `edgar` (company filings), `avalon` (founding documents).

## Oceania

Polynesian settlement (dates revised later by recent radiocarbon work), Aboriginal Australian history, contact
and colonisation. `trove` needs a key and approval (link-out); use `openalex`, `wikidata`, museum records. Memory
is weak here; say so.

## Modern and contemporary world (1800 onwards)

Wars, states, people, companies. `wikidata`, `loc`, `tna`, `avalon`, `federal-register`, `wayback` (what a web
page said and when), `edgar` (US company filings, the record for founding and incorporation dates), `chm`
(computing oral histories). For recent decades, prefer filings, archived pages and contemporary reporting over
later retellings; anniversaries and press pages restate, they rarely prove.
