# CK ACCEPTANCE FIXTURE — CAPABILITY CHECKLIST + THREE SLICES (2026-09-08)

Vervolg op artifact 97 (reconciliatie 7/9). Jef-correcties verwerkt: 35×MERGE en FAQ-redirects = **consultant hypothesis**, geen platformbeslissing; `0 GSC != MERGE`; redirect alleen na SOURCE INTENT → TARGET PAGE → ANSWER PRESENT → CONTENT PARITY. CK = tweede acceptance-fixture naast SAH. Acceptance = Sherlock observed → modelled → decided → composed → Watson rendered → browser accepted → tracking attached.
Bewijs vandaag: prod `0aa0c8b01`, ontology v13 (PATCH), tracking segments 2–5 (REST), page decisions herberekend 10:55 UTC (set `5592df4c…`, 211 rijen), `get_pages` (74 rijen), SQL topics/site_pages.

## A. CAPABILITY CHECKLIST (gereconcilieerd met bestaand werk)

| # | Capability | Status | Bewijs (CK) | Bestaand werk | Routering |
|---|---|---|---|---|---|
| 1 | Realization modelling (proof entity: locatie × dienst × probleem→oplossing × assets) | **MISSING** | `site_pages` bevat 0 van de 35 `/projecten/<slug>/` (74 rijen, wel 4 losse .webp-bestanden als "pagina"); `get_stored_pages` → `crawled:false`; Watson-CPT `realizations` + taxonomie `locations` bestaan, nooit gevoed | geen WI; Watson-theme primitief (B) | NIEUW seam onder #284 (umbrella): PROOF ENTITY = **WI #291**. Zie C. |
| 2 | Location/service relationship (geo-gekwalificeerde demand unit → surface) | **WRONG_SEMANTICS** | na geo_coverage v13 + recompute: Mol/Westerlo/Kasterlee/Herentals (concept_type `location`, aangemaakt 7/9 23:43 uit service_areas) → **create_new `/mol/`, `/westerlo/`…** met axes `money_keyword, has_demand, offering_grounded`; 7× "<gemeente> Badkamerrenovatie" → create_new; Geel/Antwerpen/Mechelen/Turnhout hebben concept_type `topic` (locatiegate ziet ze niet); `evidence.py:46` zegt "location NEVER earns a surface" | #282 (demand→cluster→page), #285 (fabricated coverage), #105 | Bewijs naar #285 + #282; de TYPE×CITY-unit bestaat alleen in tracking_segments, niet als input van de page-decision-engine → NIEUW seam onder #284: GEO-QUALIFIED DEMAND UNIT → SURFACE DECISION = **WI #292** |
| 3 | URL-level KEEP/IMPROVE/MERGE/redirect decisions | **PARTIAL** | decisions zijn per topic met `covered_by_page_id`; merges 1344/1345 verwijzen naar FAQ-page-id's zonder redirect-target; "keep Renovatie op `/faq/hoe-verloopt…/`" = topic-op-URL, geen URL-verdict; geen inputs indexeerbaarheid/uniciteit/links/backlinks/cannibalisatie | #105, #276 (second decider), #283/#286 (readiness per action) | Bewijs naar #105: URL-verdict met redirect-target + parity-inputs is de ontbrekende laag; geen nieuw WI |
| 4 | Composition bound to decision | **MISSING** | `composition_briefs.page_decision_id` bestaat niet op prod; `compose_page_plan` neemt alleen `keyword` (geen decision-input); brief 47 gebonden aan FAQ-URL i.p.v. `/premie/` | #272 (composition for EXISTING page from decision), #161/#162 | Bewijs naar #272; geen nieuw WI |
| 5 | Ordered section composition | **EXISTS_NOT_CONSUMED** | `blueprint.sections` = SERP-koppenlijst (5–12) zonder volgorde-/rolsemantiek; volgorde = MCS-2 | #161 (concept model), #162 (generator), #113 | Bewijs naar #161; geen nieuw WI |
| 6 | FAQ-to-page allocation | **WRONG_SEMANTICS** | engine: 16 SUPPORT_WITHIN_PAGE-topics op `/inloopdouche/` (o.a. "Inloopdouche Maken", "Plaatsen Van Inloopdouche") maar geen binding aan de bron-FAQ (`/faq/zelf-inloopdouche-plaatsen/`, 8.204 impr) en geen tekstbron; FAQ-URL's krijgen zelf KEEP-decisions als topic-drager; intent-laag vervuild (FR-termen, 'servies', 'airconditioning' als hypothese-intents) | #272, #111 (universe integrity), #125 (intent gate) | Bewijs naar #272 + #111; geen nieuw WI |
| 7 | Proof/media binding | **MISSING** | `required_blocks` "Productbeelden" = instructie, geen asset-id; tracking-segment surfaces matchen .webp-bestanden als pagina's | Visual-communication lane (CLOSED, doctrine ARTIFACT+INPUT), #163 | Onderdeel van seam 1 (proof entity draagt assets); geen apart WI |
| 8 | Internal-link target generation | **MISSING** | `internal_link_targets` = 0 in alle briefs; geen producer; auditor leest linkgraaf niet | #271 (site_links edges) | Bewijs naar #271; geen nieuw WI |
| 9 | Local demand + geo coverage | **EXISTS_AND_WORKS** (demand) / **PARTIAL** (coverage) | segment 2 "renovatie, badkamer, Geel": 285 impr/90d, UNDER_COVERED (topsurface = GBP-utm-home, 0 % op een site-pagina), `/badkamer-renovatie-geel/` = NEEDS_JUDGEMENT zonder rationale; `page_decisions_recomputed:false` | tracking_segments (live), #282 | Werkt als observatie; de brug naar een beslissing = seam 2 |
| 10 | Strategy/territory consumption (BADKAMERGEVOEL, bad→douche ≠ "veilige douche"-zoekterritorium) | **EXISTS_NOT_CONSUMED** | findings 72–76 CLIENT-APPROVED; geen lezer in decision/brief/composer; MCS-9 | #161, Brand&Demand spine (#1274/#1275) | Bewijs naar #161; geen nieuw WI |

Operator-gaten gevonden tijdens de slice (MANUAL OPERATOR GAP):
- MCP `create_tracking_segment`: tool declareert geen input-schema (`additionalProperties`), waardoor het geneste `definition`-object als string aankomt → "Input should be a valid dictionary". REST `/api/explorer/{site}/segments` werkt wel. → #164 (MCP tool defects).
- MCP `update_client_ontology` kent geen `geo_coverage`/`headquarters`; alleen de REST-PATCH kan dat schrijven → #164.
- MCP `list_search_intents` negeert `query`; `recompute_page_decisions`/`list_page_decisions`/`get_pages` overschrijden de 25k-token-grens zonder paginering → #164.
- Geen UI voor tracking segments (grep frontend = 0) → #282.

## B. DRIE ACCEPTANCE SLICES — resultaat

### B1. GEO/PROOF — Geel + realisatie Geel + bad→douche
| Stap | Klasse | Resultaat |
|---|---|---|
| Sherlock observed | A | GSC-demand Geel: 4 TYPE×CITY-voorstellen; segment 2 bewijst 285 impr, 1 click, pos 18, landend op GBP-home |
| Sherlock modelled | A/PARTIAL | ontology v13: HQ Geel + geo_coverage (10 areas) via PATCH; locatie-topics deels `location`, deels `topic` |
| Sherlock decided | **FAIL (WRONG_SEMANTICS)** | recompute: Geel → needs_judgement (container `/`), Mol/Westerlo/Kasterlee/Herentals → **create_new stadspagina's**; `/badkamer-renovatie-geel/` (10421) krijgt 0 decisions; geen TYPE×CITY→surface-beslissing |
| Sherlock composed | NIET BEREIKT | brief 44 blijft zonder decision-binding |
| Watson rendered / browser / tracking | — / — / A | segments 2–5 aangemaakt; tracking is klaar om na launch te meten |
**EARLIEST BREAK = DECIDE**: de demand unit die de vraag draagt (TYPE×CITY) is geen input van de page-decision-engine; de engine ziet alleen topics en projecteert locatie-topics op stadspagina's.

### B2. FAQ→MONEY — `/faq/zelf-inloopdouche-plaatsen/` (8.204 impr) → `/inloopdouche/`
| Stap | Klasse | Resultaat |
|---|---|---|
| observed | PARTIAL | GSC per URL ok; de FAQ-URL staat als rij in `site_pages` (page_type supporting, H1 leeg) maar `get_stored_pages` → crawled:false: geen body-tekst, dus geen antwoord-parity meetbaar |
| modelled | PARTIAL | topic "Inloopdouche Maken"/"Plaatsen Van Inloopdouche" bestaan; geen intent "zelf plaatsen"; intent-laag vervuild |
| decided | PARTIAL | 1194/1205 SUPPORT_WITHIN_PAGE op `/inloopdouche/` — juiste doelpagina, maar zonder bron-URL, zonder tekstbron, zonder parity-check |
| composed | **FAIL (MISSING)** | geen composition-for-existing-page uit een decision (#272); `compose_page_plan` is keyword-only |
| rendered / accepted / redirect | NIET BEREIKT | daarom: **geen FAQ-redirect bij launch**; FAQ-URL's blijven 1:1 bestaan (parity) |
**EARLIEST BREAK = COMPOSE** (decision → sectie op bestaande pagina).

### B3. REALISATION — `/projecten/project-geel-bad-naar-douche/`
| Stap | Klasse | Resultaat |
|---|---|---|
| observed | **FAIL (MISSING)** | 0 van 35 realisatie-URL's in `site_pages`; crawl heeft de detailpagina's nooit opgeslagen (wel 4 .webp-bestanden als pagina) |
| modelled → decided → composed → links | NIET BEREIKT | geen proof-object; Watson-CPT `realizations` + `locations` ongevoed |
**EARLIEST BREAK = OBSERVE**.

## C. GENERIC SEAMS die ontbreken (search-before-create op 119 open WIs: geen match op realis*/proof/geo-demand) — aangemaakt als WI #291 (proof entity) en WI #292 (geo-qualified demand unit); CK-bewijs gepost op #285, #272, #105, #164, #271, #161, #282 (notificaties 9–15); artifacts 97 + 98
1. **PROOF ENTITY**: realisatie als object (locatie, regio, dienst/offer-ref, probleem, oplossing, assets, datum, bron-URL, provenance) — geobserveerd uit crawl (WP-CPT/JSON-LD/URL-patroon) of intake; Watson-CPT `realizations` als render-doel. Decision-laag kiest expressie: OWN DETAIL PAGE / COLLECTION ENTRY / SUPPORT_WITHIN_SERVICE_PAGE / SUPPORT_WITHIN_LOCATION_PAGE / MERGE / NO_SURFACE, met inputs indexeerbaarheid, unieke content, uniciteit locatie×dienst, interne links, externe provenance, lokale vraag, cannibalisatie, authority-waarde.
2. **GEO-QUALIFIED DEMAND UNIT → SURFACE DECISION**: TYPE×CITY-segment (of offer × geo_coverage) als demand unit in de page-decision-engine, met uitkomsten REALISATION_ONLY / SUPPORT_WITHIN_SERVICE_PAGE / LOCATION_COLLECTION / CREATE_LOCAL_SERVICE_SURFACE / NO_SURFACE / NEEDS_JUDGEMENT — nooit `location`-topic → stadspagina.
Alles anders (URL-verdict + parity, composition-from-decision, sectievolgorde, FAQ-allocatie, links, media, territory) heeft een bestaande owner (#105, #272, #161, #162, #271, #285, #282, #164) en krijgt alleen CK-bewijs.

## D. CLIENT DELIVERY (parallel, launchbaar zonder brede URL-migratie)
- 22 FAQ-URL's en 35 realisatie-URL's blijven **1:1 bestaan** op de launch-site (+ `/projecten/` overzicht); alle FAQ→dienst-redirects verwijderd tot parity per URL bewezen is. `/voor-en-na/` → `/onze-projecten/` blijft (inhoud aanwezig). 
- Geen nieuwe secties op dienstpagina's uit CC-hand (dat is B2's compose-stap; die hoort Sherlock te leveren).
- 35×MERGE en FAQ-tabel §12 van 7/9 = HYPOTHESE; heropenen zodra seam 1/2 en #272 bewijs leveren.
