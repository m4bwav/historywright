# Creation pass 2026-10-17: practice (raw researcher report)

Verbatim report of the evergreen-researcher pass for this track. Synthesis: [../2026-10-17-creation-pass.md](../2026-10-17-creation-pass.md).

## Findings (newest first)

### F1 · 2026-09-14 · AskHistorians moderator: AI answers drown out experts, and AI accusations hit real people
- What: Sarah Gilbert, a Cornell researcher and r/AskHistorians moderator, writes that since late 2022 AI content "takes the oxygen" from expert answers. The sub removes it as low-effort content, allows some disclosed AI use, bans undisclosed use and has an appeals process. She also says moderators have wrongly banned real users they took for bots. In 2023 Vice reported 5 to 10 ChatGPT posts a day on the sub soon after launch.
- Track: practice
- Affects: output framing and disclosure (the answer format; any "post this to a forum" use)
- Magnitude: n/a (initial)
- Suggested response: note. Guard: every answer labels itself as AI-researched and lists its sources, and the skill never presents output as an expert's answer for posting.
- Sources: https://techpolicy.press/millions-of-volunteers-are-keeping-the-internet-human-for-now, https://content.fromthepage.com/chatgpt-r-askhistorians-spam/

### F2 · 2026-08-29 · "AI Historian" agent: anchoring to source sentences beats direct prompting on chronology, 86% to 17%
- What: Lu et al. (arXiv 2608.29133) built an agent that treats each source sentence as a unit of evidence, extracts people and time cues, and infers time ranges with each claim tied to its sentence. On six Shiji cases it scored 86.2% temporal-localisation MicroIoU in about 14 minutes. Human-only annotation scored 81.3% in about 92 minutes, and direct LLM prompting scored 17.1%. The sample is small (six cases).
- Track: practice
- Affects: the timeline export in research packs; the "answer from memory" path
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: every timeline row carries the quoted source sentence and a date range (not a point date), and the skill never builds a timeline by asking the model for dates.
- Sources: https://arxiv.org/abs/2608.29133

### F3 · 2026-05-27 · Humphries: a second model family catches 76% of transcription errors, but shared errors survive
- What: Mark Humphries had Gemini 3.5 Flash and Claude Opus 4.7 re-transcribe pages first done by Gemini 3 Pro, and a human reviewed every passage where they disagreed. That caught 106 of 139 errors while the human read only about 4% of the text. The 33 errors left were ones all three models made: about a third were spelling modernisations ("Moose" for "Mooss"), about a third were page numbers or damaged text, and the rest were misread dates and numbers, insertions and deletions.
- Track: practice
- Affects: the quote-verification step; primary-text handling
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: when a quote or date comes from a scan or OCR, check it with a second model family and show the disagreements. Never silently modernise spelling inside quotation marks. Give dates and numbers from scans a "read from image" tag.
- Sources: https://generativehistory.substack.com/p/when-models-disagree-transcription

### F4 · 2026-05-12/19 · Nonfiction book ships with AI-fabricated and misattributed quotes that passed the publisher's fact-check
- What: Steven Rosenbaum's *The Future of Truth* (Matt Holt Books, distributed by Simon & Schuster) contained synthetic quotes attributed to Kara Swisher, Lisa Feldman Barrett and others. He used ChatGPT and Claude, and the publisher's fact-checker did not catch the fabrications. The book is not history, but the failure (a plausible quote from a real person) is the most common one in history writing.
- Track: practice
- Affects: the quote and citation rules in the answer format
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: a direct quote may appear only if its exact words were found in a fetched text that names the speaker. Otherwise paraphrase it and mark it "attributed, unverified". An eval case should plant a famous misattributed quote.
- Sources: https://oecd.ai/en/incidents/2026-05-19-f57e, https://incidentdatabase.ai/entities/people-misquoted-by-ai-assisted-books/

### F5 · 2026-04-27 · ProHist-Bench (ACL 2026): 18 LLMs fall short on evidence-based historical reasoning
- What: Gao et al. built 400 expert questions on the Chinese imperial examination system across eight dynasties, scored with 10,891 rubric items. They test higher-order skills (evidence-based reasoning), not recall. All 18 models show a "significant proficiency gap". The abstract gives no headline numbers and I did not read the full paper.
- Track: practice (also testing)
- Affects: the confidence line; when to trust model reasoning
- Magnitude: n/a (initial)
- Suggested response: note. Guard: interpretive claims ("why X happened") must cite a historian who argued it, not the model's own synthesis.
- Sources: https://arxiv.org/abs/2604.24690

### F6 · 2026-04-17 · Humphries on agents: they stop early, loop, and one free-ChatGPT list of ten sources included one that does not exist
- What: In "The Agents Are Waking Up", Humphries reports Claude Cowork (Opus 4.6/4.7) is good at assembling material and finding open-licence images with citations, but it "tends to stop before the task is fully complete" and sometimes falls into loops. A free ChatGPT list of ten sources on Canadian Confederation included one that does not exist. He argues the model "can't self verify", so checking stays external.
- Track: practice
- Affects: research-pack export (completeness); the self-check step
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: the pack export runs a completeness checklist (entities, places, timeline, images, sources, each present or marked empty with a reason), and verification is done by a script or a separate pass, never by the drafting model alone.
- Sources: https://generativehistory.substack.com/p/the-agents-are-waking-up

### F7 · 2026-03 (guideline) / Dec 2023 onward (project) · WikiProject AI Cleanup: real but unsupporting sources are now the main failure
- What: The project page reports that recent models "usually cite real sources but often don't verify that they support the content". It also documents fake foreign-language sources (the "Leninist historiography" article cited Russian and Hungarian works that do not exist) and off-topic real sources (Estola albosignata). The Amberlihisar hoax article passed Articles for Creation in January 2023 and was not unmasked until December 2023. Since March 2026, WP:LLM forbids LLM-generated or LLM-rewritten article content. A 2024 study found about 4.4% of new English Wikipedia articles from August 2024 had significant AI text.
- Track: practice
- Affects: the citation-verification step; how Wikipedia is treated as a source
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: checking that a URL resolves is not enough. The fetched source text must contain the claim (a claim-support check). Wikipedia is a finder, never the cited authority: cite its underlying reference after reading it. Treat Wikipedia text added after 2022-11-30 that rests on unfamiliar foreign-language books with extra suspicion.
- Sources: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup, https://signpost.news/2024-10-19/Recent_research

### F8 · 2026-01-21 · About 100 hallucinated citations in NeurIPS 2025 accepted papers, many of them "blended"
- What: GPTZero checked 4,841 accepted NeurIPS papers and confirmed at least 100 hallucinated citations across 51 papers, all past three or more reviewers. In a 300-paper sample of ICLR 2026 submissions, 50 had at least one. Many fakes blend real authors with plausible invented titles. The figures are the vendor's own and not independently replicated.
- Track: practice (also testing)
- Affects: the citation-verification step
- Magnitude: n/a (initial)
- Suggested response: point. Guard: look up each book or article reference in a catalogue (Crossref, Open Library or WorldCat, the publisher page) and match title, author and year together, so a real author on a fake title fails.
- Sources: https://gptzero.me/news/neurips/, https://www.theregister.com/2026/01/22/neurips_papers_contaiminated_ai_hallucinations/

### F9 · 2025-11 · Grokipedia: AI encyclopedia with weak sources and factual errors in historians' own entries
- What: Cornell Tech researchers (Triedman and Mantzarlis) found thousands of citations to "questionable" and "problematic" sources. Richard Evans found false claims in the Hobsbawm entry (that he lived through the 1923 hyperinflation, and about his military service). PolitiFact found most articles copied from Wikipedia, with unsupported additions.
- Track: practice
- Affects: the source-tier list
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: block AI-generated encyclopedias (Grokipedia and similar), AI "history" sites, and content farms as evidence. They may only be listed as leads.
- Sources: https://scour.ing/p/https://www.theguardian.com/technology/2025/nov/03/grokipedia-academics-assess-elon-musk-ai-powered-encyclopedia, https://api.politifact.com/article/2025/nov/12/Grokipedia-Wikipedia-AI-citations

### F10 · 2025-11 · Multimodal LLM OCR modernises archaic spelling and inserts characters from the wrong period
- What: Levchenko (Anthology of Computers and the Humanities, vol. 3) tested 11 multimodal LLMs on 1,030 pages of 18th-century Russian print. They beat classic OCR on character error rate, but modernised archaic spelling and sometimes inserted medieval Slavonic characters that do not belong. This matches the residual errors in F3.
- Track: practice
- Affects: primary-text quotes; museum-label and inscription transcriptions in packs
- Magnitude: n/a (initial)
- Suggested response: note. Guard: mark machine transcriptions as such, keep the original spelling, and prefer a published edition's text over your own OCR.
- Sources: https://anthology.ach.org/volumes/vol0003/building-historical-corpora-with-multimodal-llms/

### F11 · 2025-09-03 · AI "Boring History" videos flood YouTube with inaccurate visuals
- What: 404 Media (Jason Koebler) documents channels such as Sleepless Historian and Boring History Bites. One two-hour video has 2.3 million views, and its narration drifts from Anne Boleyn to 1770s America inside a "medieval" video. Historians cite glazed windows and train tracks in 1300s scenes, and modern bread in Pompeii. BOOM Live found viral Indian AI history reels inventing events, such as a fake relationship involving a Mughal princess.
- Track: practice
- Affects: the image-reference step in packs; the source-tier list
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: reference images come only from museum or collection records with an accession number and the object's own date, never from image search, video stills or social media. Video and social posts are never evidence.
- Sources: https://www.404media.co/ai-generated-boring-history-videos-are-flooding-youtube-and-drowning-out-real-history/, https://www.boomlive.in/decode/ai-history-videos-india-reels-youtube-viral-29514

### F12 · 2025-08-05 · AHA Guiding Principles for AI in History Education name the unacceptable shortcuts
- What: The American Historical Association's principles were approved by its Council on 2025-07-29. They say: "Generative AI regularly hallucinates content, references, sources, and quotations"; "any information provided by a generative AI tool could be false unless properly verified"; and "AI introduces a false sense of certainty where uncertainty exists". The policy table marks two practices "Never acceptable": putting an AI-generated reference in a footnote without checking the original, and relying on an AI summary without reading the source. It also calls AI images of the past "fabrications, not authentic reconstructions".
- Track: practice
- Affects: the core rules; the confidence line; image packs
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: cite only what was fetched and read during this run. The confidence line must say what is uncertain or contested (uncertainty is a normal result, not a failure). Generated images are labelled reconstructions, kept apart from museum references.
- Sources: https://historians.org/AI-history-education

### F13 · 2025-05-23 · Eight chatbots tested: only 26.5% of generated references fully correct
- What: Cabezas-Clavijo and Sidorenko-Bautista (J. Data & Information Science, 2026) scored 400 references from the free tiers of ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat and Perplexity, humanities included. 26.5% were fully correct, 33.8% partly correct, and 39.8% wrong or invented. Journal articles were fabricated far more often than books. Claude, Copilot and Perplexity had the highest hallucination rates. Earlier work: 55% of GPT-3.5 and 18% of GPT-4 citations were fabricated (Walters & Wilder 2023). A GPT-3.5 humanities sample had 89% of its DOIs hallucinated.
- Track: practice
- Affects: the "no references from memory" rule
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: never output a reference the run did not retrieve, and never output a DOI that was not resolved. An eval case should ask for "five key books on X" and check each one against a catalogue.
- Sources: https://arxiv.org/abs/2505.18059, https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980

### F14 · 2025-05-18 (rev. 2026-02-20) · HistVis: image models stereotype eras and insert anachronisms (cf. Gemini, Feb 2024)
- What: De Rosa Palmini and Cetinic generated 30,000 images of everyday activities across periods with three diffusion models. The models stereotype eras through unstated style cues, add anachronisms, and get period demographics wrong. A Malmö University study found mobile phones in "1936" photos. In February 2024 Google paused Gemini's images of people after historically wrong depictions; Prabhakar Raghavan said tuning made it "overcompensate in some cases… embarrassing and wrong". DW's fact-check quotes historian Sebastian Kubon's test: could this thing have existed at that time?
- Track: practice
- Affects: the image prompts and anachronism check that the packs feed into 3D and video work
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: each pack carries a per-period anachronism checklist (clothing, weapons, architecture, materials, glazing, lighting, writing) built from cited sources. Prompts state the period constraints and the demographics from sources. The downstream check asks of every visible object whether it could have existed then and there.
- Sources: https://arxiv.org/abs/2505.17064, https://mau.se/en/news/AI-produces-stereotypical-and-anachronistic-images-when-portraying-the-past/, https://9to5google.com/2024/02/23/gemini-image-generation-google-statement/

### F15 · 2025-04 · Underwood, Nelson & Wilkens: prompting cannot remove anachronism from "period" text
- What: Prompting a current model with period prose did not give period-consistent style. Fine-tuning fooled an automated judge but not human readers. The authors suggest only pretraining on period text may work.
- Track: practice
- Affects: any "period voice" or dialogue output for video scripts
- Magnitude: n/a (initial)
- Suggested response: note. Guard: label generated period dialogue as pastiche, and source any real period phrasing from quoted primary texts.
- Sources: https://arxiv.org/abs/2505.00030

### F16 · 2025-02-19 (updated 2026-01-07) · FutureSearch audit of OpenAI Deep Research: overconfidence, odd source choice, silent omission
- What: The audit found Deep Research gave wrong figures without hedging and used a weak source over an authoritative one it had already found. It credited Statista where it had the original PDF, and sought corroboration from Reddit instead of Our World in Data. It returned 34 of 45 table rows with no sign that any were missing, and blurred confirmed facts with speculation.
- Track: practice
- Affects: the source-ranking and confidence rules; the sources-disagree note
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: rank sources by tier (primary or edited primary, then peer-reviewed or academic press, then museum or archive, then reputable reference, then everything else) and cite the original, not the aggregator. Say what was not covered. Keep "sources say" apart from "inferred".
- Sources: https://futuresearch.ai/blog/oaidr-feb-2025/

### F17 · 2025-02-07 · Humphries tests Deep Research on fur-trade history: good bibliography, fabricated quotes and claimed analyses it never ran
- What: Deep Research did well on historiography and on surveying archives: "exactly what I would expect from a human RA". On a text comparison it claimed n-gram analysis, but its code gave "wildly off" numbers, and "many of the quotes… were either entirely made up or poorly paraphrased". When he asked for qualitative analysis only, "the citations all worked and the quotations were accurate".
- Track: practice
- Affects: the rules on methods and quotes
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: never claim a count, statistic or "analysis" that was not computed in this run with the code shown, and keep to what the fetched texts support.
- Sources: https://generativehistory.substack.com/p/is-this-the-last-generation-of-historians

### F18 · 2024-12 (NeurIPS 2024 D&B) · HiST-LLM: best model 46% on expert history facts, worst for Sub-Saharan Africa and Oceania and for recent periods
- What: The benchmark uses 36,000 Seshat data points across about 600 polities. In Table 1 (4-choice balanced accuracy), GPT-4-Turbo scores 46.0, GPT-4o 44.7, Llama-3.1-70B 40.8, Gemini-1.5-flash 39.0, GPT-3.5 35.6 and Llama-3.1-8B 33.6, against a 25% chance rate. The body text says 43.8%, so cite Table 1. On present/absent questions (2-choice) scores are 57.6 to 63.2 against 50% chance. Accuracy falls toward the present (GPT-4-Turbo 55.3% for 8000 to 6000 BCE, 38.7% for 1500 to 2000 CE). The Americas score best, Oceania and Sub-Saharan Africa worst. The data rests mostly on English sources, and only 14,000 of the 36,000 points are expert-reviewed.
- Track: practice (benchmark, also testing)
- Affects: the confidence line; when model memory may be used at all
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: model memory is never evidence for specific facts about societies. Use it only to plan searches. Lower the default confidence for Africa, Oceania and non-English-literate regions, and require at least one non-English or regional scholarly source there when possible.
- Sources: https://proceedings.neurips.cc/paper_files/paper/2024/file/38cc5cba8e513547b96bc326e25610dc-Paper-Datasets_and_Benchmarks_Track.pdf

### F19 · 2025 (ACL 2025; ICLR 2025) · Temporal-reasoning benchmarks: models recall dates by memorisation and miss time spans
- What: ChronoSense (Islakoglu et al., 16 tasks on interval relations and date arithmetic, partly from Wikidata) finds weak, inconsistent performance and signs of memorisation. ChroKnowledge (ICLR 2025, 66k items) finds models recall timestamped facts but miss the full start and end of a time span.
- Track: practice (also testing)
- Affects: the timeline builder; date arithmetic
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: do date arithmetic in code (reign lengths, ages, BCE/CE crossings, Julian/Gregorian conversion), and store start and end with their own sources.
- Sources: https://arxiv.org/abs/2501.03040, https://arxiv.org/abs/2410.09870

### F20 · 2026 (AI and Ethics, Springer) · The language of the prompt changes the framing of a contested event
- What: A qualitative case study of 1922 in Asia Minor found GPT-4o and Claude 3.5 changed terminology, who was blamed and the framing depending on the prompt language ("algorithmic mirroring"). It is a single-case design and I could not read it (paywall). Long-tail surveys (arXiv 2602.16201) report a similar Global North recall advantage.
- Track: practice
- Affects: the "sources disagree" note
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: for contested or national-narrative topics, search in the languages of each party and report each side's account by name in the sources-disagree note.
- Sources: https://link.springer.com/article/10.1007/s43681-026-01138-8, https://arxiv.org/abs/2602.16201

### F21 · ongoing (Wikipedia list) · Citogenesis: books, newspapers and museums copied Wikipedia errors, which were then cited back
- What: Documented cases include "Alan MacMasters, inventor of the toaster" (from 2012 to 2022; it entered more than a dozen books and the Hagley Museum, and Google still showed it after deletion). Others: Arthur Meighen "attended Osgoode Hall" (a 2012 newspaper citation, likely copied from Wikipedia); Bazalgette's sewer-pipe anecdote (2007 to 2021, repeated by the Institution of Civil Engineers); the "Stalin's bathroom" nickname, restored from "reliable" citations after its author tried to remove it.
- Track: practice
- Affects: the independence check before claiming corroboration
- Magnitude: n/a (initial)
- Suggested response: adopt. Guard: two sources agree only if they are independent. A news or book source dated after the claim appeared online that gives no source of its own is not corroboration. Trace the earliest source, and prefer sources that predate the claim's first appearance on Wikipedia.
- Sources: https://en.wikipedia.org/wiki/Wikipedia:List_of_citogenesis_incidents, https://en.wikipedia.org/wiki/Circular_reporting

### F22 · 2023 · Historians' early lessons: better models make errors harder to spot; retrieval over the historian's own corpus works
- What: Coghlan and Ludgate's IEEE Annals paper (2023) catalogued "ChatGPT's astonishing fabrications" about Percy Ludgate. On the SIGCIS list one author argued that a model that is usually right is a riskier assistant, because its errors are harder to catch. Gonzalez Garcia and Weilbach (CHR 2023) show retrieval over a specialist corpus as a usable research-assistant pattern. Devereaux's ACOUP post "Collections: On ChatGPT" (2023-02-17) is the most-cited historian critique; I did not read it in full.
- Track: practice
- Affects: verification policy as models improve; an optional local-corpus mode
- Magnitude: n/a (initial)
- Suggested response: point. Guard: never relax verification because a newer model "seems accurate", and offer a mode that researches only the user's own PDFs and notes.
- Sources: https://lists.sigcis.org/archives/list/members@lists.sigcis.org/thread/UADF3CKDSDIO3KUXSZRRVLWEDCISW4YF/, https://arxiv.org/abs/2310.10808, https://notes.baldurbjarnason.com/2023/02/17/collections-on-chatgpt.html

## Overall magnitude: n/a (initial). The guards most often confirmed across sources: verify a quote by its exact words in a fetched text (F4, F12, F17); check that a source supports the claim, not just that it exists (F7, F8, F13); never answer from memory (F2, F13, F18); museum-only image references with an anachronism checklist (F11, F12, F14).

## Open questions:
- Resolved: HiST-LLM headline is 46.0 (Table 1), not 43.8 (body text); regional gap confirmed (Oceania and Sub-Saharan Africa worst).
- Resolved: Humphries has written on agentic research (Feb 2025 Deep Research test; Apr 2026 agents post; May 2026 cross-model verification).
- New: no systematic, history-specific study of fabricated-citation rates exists; the evidence comes from multidisciplinary studies plus anecdotes. A small eval of our own would be original.
- New: no published benchmark for quote misattribution found; the skill needs its own eval cases.
- Still open: the exact current AskHistorians AI rule text (reddit.com is blocked here; RSS or wiki read needed).
- Still open: the full text of the Springer language-framing paper (paywalled) and Devereaux's 2023 post.
- Still open: a Programming Historian LLM lesson from 2025 or 2026 (none surfaced).

## Search plan notes:
- Practice queries that worked: Humphries' Substack archive fetch (best single source); "historians test OpenAI Deep Research"; the WikiProject AI Cleanup page fetched directly; Wikipedia's List of citogenesis incidents; "AI generated fake history YouTube"; "anachronism large language models arxiv"; the NeurIPS PDF read with the local PDF reader (WebFetch returned binary).
- Noise: queries with acoup.blog or Devereaux returned law firms. Use `site:acoup.blog` or fetch the post. HN searches surfaced nothing; try hn.algolia.com directly next time. Quote-attribution searches surfaced spam quote sites.
- Better sources found: techpolicy.press (an AskHistorians moderator); futuresearch.ai (a dated audit of Deep Research); anthology.ach.org (Computational Humanities proceedings); incidentdatabase.ai and oecd.ai incidents for dated failure cases.
- Forums the plan lacked: r/AskHistorians rules wiki (via RSS), H-Net / H-Digital, the SIGCIS mailing list, the Wikipedia AI Cleanup talk page.

## Tracks covered: subject: 0 queries (other pass) · tooling: 0 (other pass) · practice: 28 queries · testing: 0 dedicated (F5, F8, F13, F18 and F19 carry testing implications)

## Upcoming events: none found with a fixed date in the practice track

## Nothing changed: no (creation mode; baseline established)

## Cost: searches 28 · fetches 16 · tool calls 47
