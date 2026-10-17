# API keys: what historywright can use and how to get them

## Summary

historywright needs no keys. A contact address in the User-Agent, a free OpenAlex key (scriptable) and a free World Historical Gazetteer token (ORCID sign-in) raise limits; hw.py keys automates what can be automated.


Written 2026-10-17 while setting up the owner's keys; checked against each service's own docs that day. This becomes the README's "Optional keys" section and `hw.py keys` in Step 2.

historywright works with no keys at all. Keys only raise limits or unlock a source. Each one is optional, free, and in the user's own name. The agent never invents an email address and never signs up for anything without the user saying yes.

## Where keys live

`~/.historywright/config.json`, outside the repository:

```json
{
  "contact": "<your address>",
  "keys": {
    "openalex": {"api_key": "...", "status": "pending_activation", "requested": "2026-10-17"},
    "whg": {"token": "..."}
  }
}
```

Environment variables override the file: `OPENALEX_API_KEY`, `WHG_TOKEN`, `HW_CONTACT`. `contact` goes into the User-Agent that every request sends, as Wikimedia, WHG, SEC EDGAR and Open Context require.

## OpenAlex (scholarly search): automated, one click by the user

What it gives: a 10× bigger daily budget ($1 a day of usage), 30 requests a second, and paging past the first page of results. Keyless use gets page 1 at a tenth of the budget.

How (fully scriptable, documented at help.openalex.org, "Getting a key for your user"):

1. Ask the user for their email address and permission to request a key in their name.
2. `POST https://api.openalex.org/api-keys` with `Content-Type: application/json`, body `{"email": "<theirs>", "name": "historywright", "agent": "<tool name>"}`, and an `Idempotency-Key` header (a fresh UUID) so a retry returns the same key.
3. The `201` response holds the key and `"status": "pending_activation"`. Save it at once.
4. OpenAlex emails the user "Activate your OpenAlex API key". The key returns `403 key_not_activated` until they click the button. The link lasts 7 days. Requesting again with the same address resends it, at most once a day.
5. Check with `GET https://api.openalex.org/rate-limit`, sending the key.

Manual alternative: make an account at https://openalex.org/signup and copy the key from https://openalex.org/settings/api-key.

Send the key as an `api_key` query parameter or `Authorization: Bearer`. Keep it out of shared code.

## World Historical Gazetteer (places worldwide): a browser step, about five minutes

What it gives: the WHG API (place lookup and reconciliation across Wikidata, GeoNames, TGN and Pleiades), 600 queries a minute and 5,000 a day. Searching the WHG website needs no account. The API does.

How (not scriptable: WHG signs in only through ORCID):

1. Open https://whgazetteer.org/accounts/login/?next=/profile/ and choose "Sign in with ORCiD".
2. No ORCID iD yet? ORCID's own page offers to register one. It is free, open to anyone (no academic affiliation needed), and asks for a name, an email and a password. ORCID creates a public researcher profile; its visibility can be set to private in ORCID's settings.
3. Signing in to WHG the first time creates the WHG account.
4. On the WHG Profile page, generate an API token and copy it into `config.json` (or `WHG_TOKEN`).

Send the token as `?token=` or `Authorization: Bearer` (the Workbench API takes the header only), always with a User-Agent that names the tool, its version and a contact. WHG's bot filter refuses generic agents such as `bot` or `test`.

Without a token, historywright uses Pleiades (ancient world), CHGIS (China), Wikidata coordinates and OpenHistoricalMap.

## Optional extras (listed for other users)

| Service | What it adds | How to get it |
|---|---|---|
| Smithsonian Open Access | CC0 museum objects and images | free key at https://api.data.gov/signup/ (instant, by email); 1,000 requests an hour |
| Europeana | European heritage records and images | free account, then https://www.europeana.eu/account/api-keys; `api2demo` works for tests |
| US National Archives (NARA) catalog | federal records | email the NARA catalog API team (address on archives.gov/research/catalog/help/api); 10,000 queries a month; terms forbid caching content |
| Semantic Scholar | abstracts, citations | request form at https://www.semanticscholar.org/product/api; keyed use 1 request a second |
| Trove (Australia) | Australian newspapers | key plus approval levels; commercial and AI uses need permission; terms have changed without notice |

Paid or gated and never queried by historywright: the ctext.org API, JSTOR, eHRAF, the Oxford Classical Dictionary, Brill's New Pauly, BBIH, CNKI, the Transkribus API.

## The owner's setup

The record of the owner's own keys (which address, when activated, file permissions) is in the owner's private notes, never here. Keys and tokens never go into the repository, its ai-docs, issues or logs.
