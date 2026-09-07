# CK REALISATION + GEO + COMPOSITION RECONCILIATION — 2026-09-07

Site `022c4841-8934-4799-9bbb-795da4028b38` · client 11 · ckservice.be · launch-repo `jefvangool/ck-service-preview` @ `a9d9568` · Sherlock prod `0aa0c8b01`.
Bewijs: GSC 2026-03-08 → 2026-09-05 (pagina-dimensie, 42 rijen = volledige lijst), 35 live realisatiepagina's gescraped (`projects_extract.json`), 22 live FAQ-pagina's gescraped (`faq/*.html`), `composition_briefs` prod (SQL), `list_page_decisions` (197 rijen), `suggest_tracking_segments` (80 voorstellen), Watson theme `origin/main`.
Classificatie per stap: **A** = SHERLOCK PRODUCT CAPABILITY (operator kan het in UI/MCP) · **B** = INTERNAL CAPABILITY (code bestaat, operator kan er niet aan) · **C** = MISSING.
Elke keuze die ik zelf nam staat gemarkeerd als **MANUAL CONSULTANT STEP (MCS-n)** en wordt in §6 verzameld.

---

## 1. CURRENT PAGE TREE

### 1a. Launch-site (Node-server, 18 URL's, `server.js PAGES`)

```
/                                   money/home        brief 45 (H1 "Badkamergevoel? Veilig douchen in 1 dag")
├─ /veilige-douche/                 money (bad→douche) brief 41
├─ /seniorendouches/                money             brief 42
├─ /inloopdouche/                   money             brief 43 (+ oude brief 20)
├─ /douchecabine/                   money             brief 22 (gebonden aan live /onze-douches/)
├─ /douche-plaatsen/                money             geen brief
├─ /badkamer-renovatie-wandpanelen/ money/support     brief 46
├─ /onze-toiletten/                 money             geen brief (stap 4, CC)
├─ /premie/                         support→money     brief 47 (gebonden aan FAQ-URL 10423, niet aan /premie/)
├─ /badkamer-renovatie-geel/        location/service  brief 44 (local_info-blok)
├─ /onze-projecten/                 proof             geen brief · geportte live pagina + 13 voor/na-paren (CC)
├─ /over-ons/                       trust             geen brief
├─ /faq/                            hub               geen brief · 26 vragen (CC-selectie uit 22 live FAQ's + reference)
├─ /contact/  /bedankt/             conversie
└─ /privacy-verklaring/ /cookiebeleid/ /disclaimer/   legal (Berlaar-adres + btw "…233" = open klantvraag)
```

### 1b. Live ckservice.be (WordPress) — wat verdwijnt

| Live URL-familie | Aantal | GSC 6 mnd (impr / clicks) | Lot op launch-site |
|---|---|---|---|
| `/`, `/?utm_source=google_business…` | 1 | 6.368/169 + 15.655/190 (GBP-knop) | `/` |
| `/onze-douches/`, `/kocoon/`, `/vervang-je-bad-…kinemagic…/` | 3 | 1.178/33 | 301 → `/douchecabine/`, `/veilige-douche/` |
| `/veilige-douche/`, `/seniorendouches/`, `/onze-toiletten/`, `/badkamer-renovatie-wandpanelen/`, `/over-ons/`, `/contact/`, `/faq/` | 7 | zie §4 | zelfde URL |
| `/onze-projecten/` | 1 | 973/13 | zelfde URL |
| `/voor-en-na/` | 1 | 1.889/35 | 301 → `/onze-projecten/` |
| `/projecten/` (+ `/page/2..4/`) | 4 | 504/2 (+20/0) | 301 → `/onze-projecten/` |
| **`/projecten/<slug>/`** | **35** | **0 rijen in GSC** (geen enkele detailpagina komt in de volledige 42-rijen lijst voor) | **NIET GEMAPT → 404 bij launch** |
| `/faq/<slug>/` | 22 | 45.983 impr / 202 clicks samen (= 55 % van alle impressies, 27 % van alle clicks) | 15 → dienstpagina, 7 → `/faq/` (blanket) |
| `/blog/`, `/blog-post/` | 2 | — | 301 → `/`, `/premie/` |
| PDF's (`/wp-content/uploads/...`) | 3 | 456/6, 524/3, 16/0 | 2 gemapt naar `/docs/`; algemene-voorwaarden-PDF **niet gemapt** |

Sherlock heeft de 35 detail-URL's als `site_pages` (crawl) maar kent ze geen rol toe: `page_role` = "resource", geen realisatie-object, geen locatiebinding (§11).

---

## 2. CURRENT REALISATION SURFACES

| Surface | Waar | Inhoud | Herkomst inhoud | Klasse |
|---|---|---|---|---|
| `/onze-projecten/` (launch) | launch-site | geportte live tekst + **13 voor/na-paren** met stadslabel (Geel, Aartselaar, Berchem, Schoten, Lommel, Diest, Hallaar, Evere, Zaventem, Gentbrugge, Destelbergen, Kerksken, Wachtebeke) | beelden = live `/voor-en-na/`; stadslabels = bestandsnamen live site; selectie = CC (**MCS-1**) | gebouwd, geen Sherlock-object erachter |
| 35 × `/projecten/<slug>/` (live) | live WP | titel, 2–3 alinea's probleem→oplossing, 1–3 foto's, gemeente in slug/titel, **geen datum** | klant | verdwijnen bij launch (404) |
| `/voor-en-na/` (live) | live WP | fotogalerij, 35 clicks/6 mnd = tweede proof-surface na home | klant | 301 → `/onze-projecten/` |
| Sherlock `site_pages` | prod | 35 crawl-rijen, `page_role`="resource" | crawl | **B**: bestaat, geen realisatie-semantiek |
| Sherlock page decisions | prod | id 2 "Inloopdouche **keep** — served by `/onze-projecten/`"; id 44/69/80 "Destelbergen/Aartselaar/Berchem **support_within_page** `/voor-en-na/`"; id 115 "service type → absorb within `/voor-en-na/`" | engine (Jaccard op topicsets) | **fout gebonden**: de engine ziet de galerij als dienstpagina voor "Inloopdouche" en als locatie-container |
| Watson theme | `WP-block-theme-bouw` origin/main | CPT `realizations` (label Realisaties), taxonomie `locations` op services/realizations/testimonials, `project_types`, `project_phases`, blok `bouw/realizations-gallery` | theme | **B**: primitief bestaat, nooit gevuld/gebruikt voor CK |

Twee van de 13 voor/na-labels (Lommel, Diest) komen **niet** voor onder de 35 realisatiepagina's: het zijn losse galerijfoto's zonder projecttekst. Bewijs dat de galerij en de detailpagina's op de live site al twee gescheiden waarheden waren.

---

## 3. WHICH HISTORICAL REALISATION URLS WERE REDIRECTED

| Historische URL | Redirect | Status |
|---|---|---|
| `/voor-en-na/` | → `/onze-projecten/` | OK (1.889 impr behouden, inhoud: 13 paren) |
| `/projecten/` | → `/onze-projecten/` | OK |
| `/projecten/page/2/`, `/3/`, `/4/` | geen | 404 (20 impr, verwaarloosbaar; wel toevoegen) |
| `/projecten/<slug>/` × 35 | **geen** | **DEFECT — 404 bij launch.** Geen GSC-demand, maar wel: (a) interne links vanuit live `/projecten/` en `/voor-en-na/` die Google kent, (b) mogelijke GBP/social-links, (c) de énige plek met probleem→oplossing-tekst per gemeente. |
| `/wp-content/uploads/2020/05/algemene-aannemingsvoorwaarden-CK-Service.pdf` | geen | 404 (16 impr; juridisch document → hoort onder `/docs/`) |

Beslissing detail-URL's: §10.

---

## 4. GSC EVIDENCE PER IMPORTANT REALISATION / FAQ URL (2026-03-08 → 2026-09-05)

Totaal site: 83.049 impr · 747 clicks · CTR 0,9 % · pos 20,6.

| URL | Impr | Clicks | Pos | Intent (uit vraag + query's) | Aandeel site-impr |
|---|---|---|---|---|---|
| `/faq/krijg-je-een-aanpassingspremie-…/` | 15.472 | 66 | 10,8 | premie/subsidie (commercieel-informatief) | 18,6 % |
| `/faq/zelf-inloopdouche-plaatsen/` | 8.204 | 10 | 25,1 | DIY-informatief | 9,9 % |
| `/faq/wat-is-japans-toilet/` | 4.911 | 14 | 25,4 | product-informatief | 5,9 % |
| `/faq/een-bad-vervangen-door-een-douche-…/` | 4.304 | 5 | 19,7 | proces (bad→douche) | 5,2 % |
| `/faq/nadelen-badkamer-renovatie-zonder-breken/` | 2.704 | 15 | 17,9 | overweging wandpanelen | 3,3 % |
| `/faq/een-wasmachine-in-de-badkamer-plaatsen-mag-dat/` | 2.559 | **49** | 9,1 | regelgeving-informatief; hoogste FAQ-CTR | 3,1 % |
| `/faq/hoelang-duurt-badkamer-renovatie/` | 2.281 | 2 | 19,0 | proces/duur | 2,7 % |
| `/faq/wat-zijn-de-voordelen-van-een-lage-douchebak/` | 1.806 | 6 | 17,1 | product | 2,2 % |
| `/faq/wat-zijn-de-voordelen-van-een-gesloten-douchecabine/` | 1.752 | 25 | 8,2 | product | 2,1 % |
| `/faq/vanaf-welke-leeftijd-…senioren-badkamer…/` | 1.464 | 3 | 20,4 | senioren-overweging | 1,8 % |
| `/faq/alleen-douche-plaatsen/` | 669 | 0 | 26,5 | dienst-scope | 0,8 % |
| `/faq/jouw-badkamer-renovatie-welke-prijs-…/` | 476 | 0 | 44,1 | prijs | 0,6 % |
| `/faq/hangtoilet-plaatsen/` | 193 | 0 | 32,4 | dienst | 0,2 % |
| `/faq/hoe-verloopt-de-renovatie-…/` | 166 | 1 | 29,5 | proces | 0,2 % |
| `/faq/wat-zijn-de-voordelen-van-een-badkamerrenovatie-door-ck-service/` | 154 | 1 | 16,9 | merk/overweging | 0,2 % |
| `/faq/in-welke-regios-is-ck-service-actief/` | 84 | 0 | 22,2 | servicegebied | 0,1 % |
| `/faq/heeft-ck-service-showroom-badkamers/` | 82 | 3 | 33,0 | showroom (navigatief) | 0,1 % |
| `/faq/kan-ck-service-mijn-douche-aanpassen-voor-senioren/` | 46 | 0 | 16,7 | dienst | <0,1 % |
| `/faq/kan-ck-service-mijn-badkamer-inrichten/` | 40 | 0 | 44,0 | dienst-scope | <0,1 % |
| `/faq/kan-ck-service-mijn-kleine-badkamer-renoveren/` | 31 | 0 | 36,8 | dienst-scope | <0,1 % |
| `/faq/kan-ckservice-een-douchestoel-plaatsen/` (+ zonder slash) | 4 | 0 | 7–12 | product | ~0 |
| `/faq/wat-zijn-de-voordelen-van-een-douchetoilet/` | 1 | 0 | 10,0 | product | ~0 |
| `/voor-en-na/` | 1.889 | 35 | 26,9 | proof/inspiratie | 2,3 % |
| `/onze-projecten/` | 973 | 13 | 11,0 | proof | 1,2 % |
| `/projecten/` | 504 | 2 | 24,2 | proof-archief | 0,6 % |
| `/projecten/<slug>/` × 35 | **0** | **0** | — | — | 0 |

Lezing: de FAQ-laag is de organische ingang van de site (55 % van de impressies); de realisatie-detailpagina's hebben nul zichtbaarheid maar dragen de enige gelokaliseerde proof-tekst. Lokale vraag (Geel 736 impr, Westerlo 187, Mol 142, Kempen 111, Kasterlee 82, Retie 33 — 90 d, query-dimensie) landt bijna volledig op de GBP-homepage, niet op een dienst- of locatiepagina.

---

## 5. COMPOSITION STATUS PER PRIORITY PAGE

Codes: **U** = COMPOSITION_EXISTS_AND_USED · **P** = EXISTS_PARTIALLY_USED · **N** = EXISTS_NOT_USED · **M** = MISSING (niets in Sherlock; inhoud = CC/reference).
Sherlock-bron per dimensie staat in de eerste kolom.

| Dimensie (Sherlock-bron) | `/` (brief 45) | `/veilige-douche/` (41) | `/seniorendouches/` (42) | `/inloopdouche/` (43) | `/badkamer-renovatie-wandpanelen/` (46) | `/premie/` (47*) | `/badkamer-renovatie-geel/` (44) | `/onze-projecten/` (geen brief) |
|---|---|---|---|---|---|---|---|---|
| PAGE ROLE (`recommended_page_type`) | U (`service_page`, door CC in brief gezet) | **N** (`guide` — fout voor money-pagina; gebouwd als money) | N (`guide`) | N (`guide`) | N (`guide`) | N (`guide`) | N (`guide`) | **M** (geen brief, geen proof-rol in Sherlock) |
| MESSAGE / BELIEF SHIFT (`strategy_findings` creative concept 72–76: BADKAMERGEVOEL, bad→douche) | P (reference-port draagt het klant-goedgekeurde concept; niet gecomposeerd uit de findings) | P (idem + gezond-verstand-brug) | P (zelfstandig blijven; brief-H1) | M (live tekst) | M (live tekst) | P (premie €1.250 als drempelverlager) | M (Kempen-tekst = CC) | M |
| SECTION ORDER (`blueprint.sections` 5–12 SERP-koppen) | **N** — volgorde door CC (**MCS-2**) | N (11 secties, niet als volgorde gebruikt) | N (10) | N (7) | N (8) | N (10) | N (12) | M |
| PROOF (`client_grounding.trust_signals`: 1 dag, premie €1.250, honderden, Kocoon/Kinedo) | U | U | U | P (feiten uit live pagina) | P (live wandpanelen-PDF/feiten) | U | U | **M** — beelden zijn proof, Sherlock heeft geen realisatie-object |
| FAQ ROLE (`required_blocks` PAA-blok; `paa_items` = 0 in prod-briefs) | P (FAQ-sectie reference) | P (`faq_block` uit live FAQ's, CC-selectie **MCS-3**) | P (idem) | M | M | P (premie-Q's uit live FAQ) | M | M |
| CTA (`cta_type` = "contextual" — geen keuze per pagina) | P (form + tel uit reference) | P | P | P | P | P | P | P |
| INTERNAL LINKS (`internal_link_targets` = 0 in álle briefs, ook 45) | **M** — mesh door CC (**MCS-4**) | M | M | M | M | M | M | M |
| MEDIA (`required_blocks` "Productbeelden/carrousel" gedeclareerd; geen asset-binding) | P | P | P | P | P (hero gewisseld door CC) | P | P | M (13 paren door CC gekozen) |
| LOCAL PROOF (`required_blocks.local_info` enkel brief 44; `geo_coverage` leeg; locatie-topics excluded) | M | M | M | M | M | M | P (NAP-blok + regiotekst; **geen** Geel-realisatie gelinkt) | **M** (stadslabels zonder locatie-object) |
| CONVERSION ELEMENTS (Kelvin plan v1: form_submit, tel_click; dataLayer `ck_form_submit`) | U | U | U | U | U | U | U | U |

\* brief 47 is gebonden aan de FAQ-premie-URL (site_page 10423), niet aan `/premie/`; `/premie/` heeft dus formeel geen brief-binding.
Extra bevinding prod: `composition_briefs.page_decision_id` **bestaat niet** (SQL-fout) → brief ↔ page decision is op prod niet verbonden. En sinds de deploy van `0aa0c8b01` staan er 11 nieuwe, ongebonden briefs (48–58) waaronder **"Brico douchecabine", "Ideal Standard Douchecabine", "Van marcke"**: concurrent-/retailmerken als eigen pagina-briefs — dezelfde fout als de 6/9-generatie (artifact 81), nu op brief-niveau.

Conclusie §5: van 80 cellen zijn er **8 U**, 26 P, 14 N, **32 M**. Wat Sherlock echt leverde per pagina: H1, seo_title, meta (content_angle), trust-feiten, en een SERP-afgeleide bloklijst. Sectievolgorde, bewijsplaatsing, FAQ-selectie, interne links, beeldkeuze en lokale proof waren consultantwerk.

---

## 6. MANUAL CONSULTANT STEPS USED

| # | Stap | Input → beslissing | Capability die Sherlock moet bezitten | Status | Owner |
|---|---|---|---|---|---|
| MCS-1 | 13 voor/na-paren kiezen en per stad labelen | live galerij + bestandsnamen → 13 kaarten | realisatie-object (locatie, dienst, voor/na-assets) | **C** (Watson-CPT bestaat = B; Sherlock-model = C) | page-decision/geo lane |
| MCS-2 | Sectievolgorde per pagina (hero → trust → aanbod → proces → proof → FAQ → CTA) | brief-blocks + reference → volgorde | composition-plan met geordende secties (blueprint.sections is SERP-koppenlijst, geen orde) | **N** (bestaat als lijst, niet als plan) | composition lane (#161/#162) |
| MCS-3 | FAQ-selectie per pagina (welke live FAQ-antwoorden op welke dienstpagina) | 22 FAQ's + GSC → 3–6 per pagina | demand→page binding voor vraag-intents (page decision SUPPORT_WITHIN_PAGE met tekstbron) | **B** (engine geeft SUPPORT_WITHIN_PAGE maar bindt aan verkeerde pagina's) | page-decision lane |
| MCS-4 | Interne link-mesh (footer, related, in-copy) | paginarollen → links | `internal_link_targets` gevuld uit silo-model | **C** (veld bestaat, 0 gevuld, geen producer) | link-graph WI #271 |
| MCS-5 | Redirect-map (35 legacy → 18) incl. FAQ→dienst | live URL's + GSC → 301 | page decision KEEP/MERGE/RETIRE per **URL** met redirect-target | **B** (decisions zijn per topic, `covered_by_page_id`; merge-decisions 185–196 verwijzen naar page-id's zonder URL) | page-decision lane |
| MCS-6 | Hero-/productbeeld per pagina | live assets → keuze | media-binding in brief (asset-id, alt) | **C** | visual-communication lane |
| MCS-7 | Servicegebied-tekst Geel/Kempen (Turnhout, Mol, Westerlo, Herentals, Retie, Kasterlee) | `market.service_areas` (9) + lokale vraag → tekst | locatie-entiteiten als data (niet excluded) | **B** (service_areas bestaat; topics Geel/Turnhout/Lier `off_niche:low_entity_distance`) | relevance/geo lane (Slice B) |
| MCS-8 | Toiletten-pagina inhoud + toilet-FAQ | live pagina + FAQ's → 5 kaarten + 4 Q's | brief voor `/onze-toiletten/` (bestaat niet) | **C** voor deze pagina | — |
| MCS-9 | `veilige douche` = badkamergevoel/bad→douche, niet het zoekterm-territorium van Zwaluw | Jef-nuance → copy-frame | positionering per demand-unit (owned territory vs high-signal) | **C** | strategy lane |

---

## 7. GEO / SERVICE RELATION MODEL (klantfeiten, uit de 35 live realisaties)

Model: REALISATION → LOCATION (gemeente) → REGION → SERVICE TYPE → PROOF (voor/na + probleem/oplossing) → RELATED SERVICE PAGE → (LOCATION SURFACE).
DATE: **op geen enkele live pagina aanwezig** → klantvraag, niet invullen.

| Gemeente | Regio | Dienst (uit titel/tekst) | Voor/na | Probleem → oplossing (klanttekst, kort) | Gerelateerde dienstpagina | Slug |
|---|---|---|---|---|---|---|
| Geel | Kempen | bad→douche | 2 | oud bad → inloopdouche | `/veilige-douche/` + `/badkamer-renovatie-geel/` | project-geel-bad-naar-douche |
| Balen | Kempen | volledige badkamer | 2 | moderne badkamer | `/inloopdouche/` | project-balen-moderne-badkamer |
| Vosselaar | Kempen | volledige badkamer | 3 | aanpassen aan modern comfort | `/inloopdouche/` | project-vosselaar-… |
| Wiekevorst | Kempen | bad→douche | 2 | moderne badkamer met inloopdouche | `/veilige-douche/` | project-wiekevorst-… |
| Hallaar | Kempen/Mechelen | seniorendouche | 2 | rugpijn → douchen zonder bukken | `/seniorendouches/` | project-hallaar-douchen-zonder-rugpijn |
| Berlaar (×2) | Mechelen | seniorendouche (marmerlook + zitje) · bad→douche in 1 dag | 2+2 | zitje; 1 dag | `/seniorendouches/`, `/veilige-douche/` | project-berlaar-… |
| Nijlen | Kempen/Mechelen | seniorendouche | 2 | zitje "voor later" | `/seniorendouches/` | project-nijlen-… |
| Putte | Mechelen | seniorendouche | 2 | veilige stijlvolle badkamer op maat | `/seniorendouches/` | project-putte-… |
| Sint-Katelijne-Waver | Mechelen | wandpanelen + douche | 2 | duurzame wandpanelen | `/badkamer-renovatie-wandpanelen/` | project-sint-katelijne-waver-… |
| Lier | Mechelen | douche (vocht/schimmel) | 2 | onderhoudsvriendelijk tegen schimmel | `/douchecabine/` | project-lier-… |
| Pulderbos | Kempen | douche plaatsen | 2 | renovatieproject | `/douche-plaatsen/` | project-pulderbos-… |
| Aartselaar (×2) | Antwerpen | bad→douche met regenkop · badkamer met ruime douche | 1+2 | bad vervangen | `/veilige-douche/`, `/inloopdouche/` | project-aartselaar-… |
| Antwerpen (×2) | Antwerpen | 2 Japanse toiletten · badkamer met wasmachine | 2+2 | douchetoilet; wasmachine-plek | `/onze-toiletten/`, FAQ wasmachine | 2-japanse-toiletten, project-antwerpen-… |
| Berchem | Antwerpen | gesloten douchecabine | 2 | nieuwe gesloten cabine | `/douchecabine/` | project-berchem-… |
| Edegem (×2) | Antwerpen | badkamer beperkt budget · douche lagere opstap | 2+2 | budget; opstap | `/premie/`, `/seniorendouches/` | edegem-…, project-edegem-… |
| Merksem | Antwerpen | seniorendouche (zitje + handgreep) | 2 | comfort | `/seniorendouches/` | project-merksem-… |
| Mortsel | Antwerpen | grotere douche | 2 | ruimte | `/inloopdouche/` | project-mortsel-… |
| Schoten | Antwerpen | regendouche | 2 | dagelijks ontspannen | `/inloopdouche/` | project-schoten-… |
| Heverlee (×2) | Vlaams-Brabant | berging→douche · bad→douche | 2+2 | douche op gelijkvloers | `/veilige-douche/` | …-project-heverlee, project-heverlee-… |
| Leuven | Vlaams-Brabant | douchecabine | 2 | droomwoning afgewerkt | `/douchecabine/` | project-leuven-… |
| Zaventem | Vlaams-Brabant | volledige badkamer | 2 | comfortabel/makkelijk | `/seniorendouches/` | zaventem-… |
| Evere | Brussel | seniorendouche (gezin) | 2 | aangepaste douche | `/seniorendouches/` | project-evere-… |
| Beveren-Waas | Oost-Vlaanderen | seniorendouche | 2 | veilig voor senioren | `/seniorendouches/` | project-beveren-waas-… |
| Destelbergen | Oost-Vlaanderen | bad→douche | 2 | comfortabele douche | `/veilige-douche/` | project-destelbergen-… |
| Gentbrugge | Oost-Vlaanderen | seniorendouche | 2 | aangepast aan bewoners | `/seniorendouches/` | project-gentbrugge-… |
| Kerksken | Oost-Vlaanderen | seniorendouche | 2 | veilige badkamer | `/seniorendouches/` | project-kerksken-… |
| Wachtebeke | Oost-Vlaanderen | bad→douche | 2 | ruime douche | `/veilige-douche/` | project-wachtebeke-… |
| De Haan | West-Vlaanderen | berging→douchekamer | 3 | extra douche | `/douche-plaatsen/` | project-de-haan-… |
| (onbekend ×2) | — | badkamer marmerlook · schimmeldouche | 3+2 | — | `/inloopdouche/`, `/douchecabine/` | project-badkamer-marmerlook, project-schimmeldouche-… |

Tellingen: per dienst — seniorendouche/veilige douche 10 · bad→douche 8 (+2 berging→douche) · volledige badkamer 6 · douche 4 · douchecabine 2 · toilet 1 · wandpanelen 1. Per regio — Kempen/Mechelen 12 · Antwerpen 10 · buiten kernregio 11 · onbekend 2.
Betekenis: het proof-zwaartepunt ligt op **seniorendouche + bad→douche** (18/35) en op de as **Kempen–Mechelen–Antwerpen** (22/35). Geel zelf heeft **één** realisatie; de Kempen-cluster (Geel, Balen, Vosselaar, Wiekevorst, Pulderbos, Hallaar, Nijlen) heeft 7.

---

## 8. PROPOSED INTERNAL LINK SILO

```
HOME /
 ├─ MONEY: /veilige-douche/  /seniorendouches/  /inloopdouche/  /douchecabine/  /douche-plaatsen/  /onze-toiletten/  /badkamer-renovatie-wandpanelen/
 │     ↕ elk money-blad linkt naar: 1 SUPPORT (premie), 2–3 REALISATIES van hetzelfde diensttype (met gemeente), 1 LOCATION CONTEXT (Geel) — geen generiek "andere oplossingen"-blok
 ├─ SUPPORT: /premie/ (→ elke money-pagina die premie-plichtig is; ← vanuit elke money-pagina)  ·  /faq/ hub (→ per vraag naar de dienstpagina die het antwoord draagt)
 ├─ PROOF: /onze-projecten/ collectie met 35 ankers (#geel-bad-naar-douche …) 
 │     elke realisatie → zijn dienstpagina (bv. Hallaar → /seniorendouches/) én → locatie-context indien die bestaat (Geel)
 │     elke dienstpagina → zijn 2–3 realisaties (bidirectioneel; geen weesgalerij)
 └─ LOCATION CONTEXT: /badkamer-renovatie-geel/ → Geel-realisatie + Kempen-realisaties (Balen, Vosselaar, Wiekevorst, Pulderbos) → money-pagina's; ← vanuit home, /onze-projecten/, footer
```

Huidige toestand (gemeten in de 14 HTML-bestanden): elke pagina linkt naar nagenoeg álle andere pagina's (footer + "Ook interessant"-blok), dus **wel bidirectioneel, maar generiek** — precies het patroon dat Jef niet accepteert. `/onze-projecten/` linkt naar dienstpagina's (5× inloopdouche, 4× premie/douchecabine/douche-plaatsen) maar **geen enkele realisatiekaart linkt naar haar dienst of gemeente**, en geen dienstpagina linkt naar een specifieke realisatie. Realisaties zijn dus vandaag een weesgalerij met een footer-link.

---

## 9. LOCATION SURFACE DECISIONS

Inputs per locatie: SERVICE AREA (`market.service_areas`: Antwerpen, Mechelen, Turnhout, Herentals, Geel, Mol, Westerlo, Kasterlee, Lier) · LOCAL DEMAND (GSC query-dimensie 90 d; TYPE×CITY-voorstellen) · REALISATIES (§7) · UNIEKE LOKALE PROOF · HUIDIGE RANKING · SERP LOCAL INTENT (brief 44: local pack rankt op "badkamerrenovatie geel").

| Locatie | Service area | Lokale vraag | Realisaties | Unieke lokale proof | Ranking nu | Beslissing | Waarom |
|---|---|---|---|---|---|---|---|
| **Geel** | HQ | 736 impr (4 TYPE×CITY-voorstellen: badkamer renovatie geel 99, geel badkamer 80, sanitair geel 62, badkamerrenovatie geel 26) | 1 (+6 Kempen) | vestiging/NAP, showroomloos, zaakvoerder werkt mee | GBP-home pos 8 | **CREATE_LOCAL_SERVICE_SURFACE — bestaat al** (`/badkamer-renovatie-geel/`); IMPROVE: Geel-realisatie + Kempen-realisaties + TYPE×CITY-tracking | local pack + HQ + vraag + proof: alle vier aanwezig |
| Westerlo | ja | 187 impr (1 voorstel, 74) | 0 | geen | GBP-home | **SUPPORT_WITHIN_SERVICE_PAGE** (Geel-pagina servicegebied) | vraag zonder proof → geen eigen surface |
| Mol | ja | 142 (voorstel 54) | 0 | geen | — | SUPPORT_WITHIN_SERVICE_PAGE (Geel) | idem |
| Kasterlee, Retie | ja / nee | 82 (27), 33 | 0 | geen | — | SUPPORT_WITHIN_SERVICE_PAGE (Geel) | idem |
| Turnhout, Herentals | ja | niet in top-vraag | 0 | geen | — | **NO_SURFACE** (alleen servicegebied-vermelding) | geen vraag, geen proof |
| Kempen (regio) | — | 111 | 7 | cluster-proof | — | SUPPORT_WITHIN_SERVICE_PAGE (Geel = Kempen-pagina) | regio-term draagt de Geel-pagina |
| **Antwerpen** (stad + Berchem, Merksem, Mortsel, Edegem, Aartselaar, Schoten) | ja | onbekend als stadsquery (geen TYPE×CITY-observatie; 19 ongeobserveerde offer×geo-voorstellen) | **10** | historische werkregio (Aartselaar-adres in Ads/decisions) | — | **NEEDS_JUDGEMENT** → voorlopig REALISATION_ONLY + LOCATION_COLLECTION-filter in `/onze-projecten/` | 10 realisaties maar HQ is verhuisd naar Geel; klantvraag: is Antwerpen nog kernmarkt? |
| Mechelen-as (Lier, Berlaar, Putte, Nijlen, Hallaar, SKW) | Mechelen/Lier ja | geen stadsquery gemeten | 7 | — | — | **REALISATION_ONLY** | proof zonder gemeten vraag |
| Leuven/Heverlee/Zaventem, Evere | nee | geen | 4 | — | — | REALISATION_ONLY | bereik-proof, geen markt |
| Gent-rand, Beveren-Waas, De Haan | nee | geen | 6 | — | — | REALISATION_ONLY | idem |

Sherlock zelf besliste voor locaties: "Mechelen → support_within_page `/`", "provincie Antwerpen / Aartselaar Geel Antwerpseweg → support_within_page `/offerte/`", "Antwerpen → keep, served by `/faq/wat-is-japans-toilet/`", "Politiezone/Brandweer Zone Antwerpen → absorb within `/`". Geen van deze is bruikbaar; Geel/Turnhout/Lier komen als topic niet eens door de gate. **Locatie-surface-beslissingen zijn vandaag 100 % consultant (MCS-7).**

---

## 10. PROJECT DETAIL SURFACES (35 historische URL's)

Sherlock page-decision-semantiek toegepast per URL: KEEP = eigen vraag + eigen bijdrage; IMPROVE = eigen vraag, dunne pagina; MERGE = geen eigen vraag, inhoud hoort in een bredere surface.
Evidence: 0 impressies voor alle 35; 1–3 foto's; 100–300 woorden klanttekst; geen datum; interne links op live site alleen vanuit archief + galerij.

**Beslissing: MERGE ×35 → `/onze-projecten/#<slug>`** met behoud van alle inhoud als **anker-entry** (groot voor/na-beeld, gemeente, dienst, probleem→oplossing, link naar dienstpagina, link naar Geel-pagina waar van toepassing). Redirect `/projecten/<slug>/ → /onze-projecten/#<slug>` (301, fragment mag). KEEP als aparte URL is niet gerechtvaardigd (nul vraag, geen unieke intentie); een aparte detail-URL wordt pas VALUABLE_POST_LAUNCH voor locaties met een surface-beslissing (nu: alleen Geel, en die proof past in de Geel-pagina zelf).
Consequentie: `/onze-projecten/` moet **alle 35 + de 2 losse galerijparen (Lommel, Diest)** tonen met filter per dienst en per regio (= LOCATION_COLLECTION), niet 13 kaarten. UI-eis van Jef (groot voor/na-beeld + context) is met de ck-pair-kaart deels gehaald maar de context (dienst, probleem, link) ontbreekt nu.
Klasse: REQUIRED_FOR_REDIRECT (35 URL's mogen bij launch niet 404'en). Dit is een **MANUAL CONSULTANT STEP (MCS-5/MCS-1)** — Sherlock levert hiervoor geen decision per URL; zijn merge-decisions 185–196 verwijzen naar page-id's zonder URL of redirect-target.

---

## 11. GEO PRIMITIVES — search-before-create

| Primitief | Bestaat? | Waar | Staat voor CK | Klasse |
|---|---|---|---|---|
| service areas | ja | `ontology.market.service_areas` (9) | gevuld (v11) | A |
| location entities | ja als topics | `topics` Geel/Turnhout/Lier/Antwerpen/Mechelen | **excluded `off_niche:low_entity_distance`** (Geel!), Antwerpen/Mechelen wel door de gate | B (data bestaat, gate sluit HQ-stad uit) |
| geo_coverage | ja | `ontology.market.geo_coverage[]` | **leeg**; enige lezer = tracking_segments | B |
| realization-by-location | **nee in Sherlock**; ja in Watson (`realizations` CPT + `locations` taxonomie) | theme | 0 objecten | C (Sherlock) / B (Watson) |
| local demand | ja | GSC query-dim + `suggest_tracking_segments` TYPE×CITY (7 geobserveerd) | Geel 4, Westerlo, Mol, Kasterlee | A |
| local page decisions | engine bestaat; geen locatie-semantiek | `list_page_decisions` | fout gebonden (§9) | B |
| tracking segments TYPE×CITY | ja | `create_tracking_segment` / `list_tracking_segments` | voorgesteld, **niet aangemaakt** | A |
| local ranking per city | nee | — | GSC-positie alleen per pagina | C |

Gecombineerd:

| LOCATION | CURRENT REALISATIONS | SEARCH DEMAND (90 d) | SERVICES PROVEN THERE | CURRENT COVERAGE | RECOMMENDED SURFACE | TRACKING SEGMENT |
|---|---|---|---|---|---|---|
| Geel | 1 (bad→douche) + 6 Kempen | 736 impr / 4 TYPE×CITY-units | bad→douche; Kempen: badkamer, senioren, douche plaatsen | `/badkamer-renovatie-geel/` (brief 44, geen realisatie gelinkt); GBP-home vangt de clicks | IMPROVE local service surface | TYPE×CITY Geel (badkamerrenovatie / badkamer / sanitair) — **aan te maken** |
| Westerlo · Mol · Kasterlee · Retie | 0 | 187 · 142 · 82 · 33 | — | tekstvermelding Geel-pagina | SUPPORT_WITHIN Geel | TYPE×CITY Westerlo, Mol, Kasterlee (voorgesteld) |
| Antwerpen-cluster | 10 | ongemeten | senioren, bad→douche, cabine, toilet, badkamer | 0 (geen surface; decisions binden aan FAQ/offerte) | REALISATION_ONLY + collectiefilter; NEEDS_JUDGEMENT klant | badkamerrenovatie × Antwerpen (voorgesteld, 0 observaties) |
| Mechelen-as | 7 | ongemeten | senioren, wandpanelen, schimmel-douche | 0 | REALISATION_ONLY | badkamerrenovatie × Mechelen/Lier (voorgesteld, 0 obs.) |
| Overige (VL-Brabant, Brussel, O-/W-Vl) | 10 | geen | senioren, bad→douche | 0 | REALISATION_ONLY | geen |

---

## 12. FAQ URL DECISIONS (22 URL's)

Criteria: GSC 6 mnd (§4) · intent · huidige inbound links (live FAQ's linken onderling nauwelijks; 9 van 22 linken naar een dienstpagina) · doel-dienstpagina · **is het antwoord vandaag op de doelpagina aanwezig?** (gemeten met grep op de launch-HTML).
Outcomes: KEEP (eigen URL herbouwen) · MERGE INTO SERVICE PAGE (301 + antwoord staat op de dienstpagina) · SUPPORT_WITHIN_PAGE (301 + antwoord **moet nog** in de dienstpagina) · FAQ HUB (301 → `/faq/#anker`, volledig antwoord daar) · RETIRE (301 zonder inhoud).

| FAQ-URL (kort) | Impr / clicks | Huidige redirect | Antwoord aanwezig op doel? | **Beslissing** | Toelichting |
|---|---|---|---|---|---|
| aanpassingspremie | 15.472 / 66 | `/premie/` | ja (€ ×7, prijs ×4; brief 47 H1) | **MERGE INTO SERVICE PAGE** `/premie/` | grootste organische ingang; `/premie/` is de opvolger. Brief 47 moet naar `/premie/` gebonden worden. |
| zelf-inloopdouche-plaatsen | 8.204 / 10 | `/inloopdouche/` | **nee** ("zelf" komt niet voor) | **SUPPORT_WITHIN_PAGE** `/inloopdouche/` — sectie "Zelf plaatsen of laten plaatsen?" toevoegen | DIY-intent op een money-pagina is alleen verdedigbaar als de vraag beantwoord wordt; anders soft-404-gedrag op 10 % van de impressies |
| wat-is-japans-toilet | 4.911 / 14 | `/onze-toiletten/` | ja (Japans ×9, FAQ-Q aanwezig) | MERGE INTO SERVICE PAGE | — |
| bad-vervangen-hoe-gaat-dat | 4.304 / 5 | `/veilige-douche/` | ja (proces + "1 dag" ×11) | MERGE INTO SERVICE PAGE | — |
| nadelen-zonder-breken | 2.704 / 15 | `/badkamer-renovatie-wandpanelen/` | **nee** ("nadel" 0×) | **SUPPORT_WITHIN_PAGE** — eerlijke nadelen-sectie op wandpanelen-pagina | 15 clicks; de vraag is de overweging vóór de dienst |
| wasmachine-in-badkamer | 2.559 / **49** | `/faq/` (blanket) | alleen als hub-vraag | **KEEP** eigen URL (herbouwen als FAQ-artikel) + link naar realisatie Antwerpen-wasmachine | hoogste FAQ-clicks en CTR 1,9 %; geen dienstpagina past; blanket-redirect gooit 49 clicks weg |
| hoelang-duurt-badkamerrenovatie | 2.281 / 2 | `/faq/` | hub-vraag aanwezig | **SUPPORT_WITHIN_PAGE** `/veilige-douche/` (1-dag-belofte) of hub-anker | proces-vraag = kern-USP; 301 naar dienstpagina met anker |
| lage-douchebak | 1.806 / 6 | `/douchecabine/` | **nee** (0×) | SUPPORT_WITHIN_PAGE `/douchecabine/` | hub heeft "lage instapdouche"-Q; op doelpagina ontbreekt hij |
| gesloten-douchecabine | 1.752 / 25 | `/douchecabine/` | ja (Gesloten ×3) | MERGE INTO SERVICE PAGE | 25 clicks, antwoord aanwezig; Sherlock-decision 55 "keep" op deze FAQ-URL is achterhaald door de merge |
| senioren-leeftijd | 1.464 / 3 | `/seniorendouches/` | **nee** ("leeftijd" 0×; wel zitje ×9) | SUPPORT_WITHIN_PAGE `/seniorendouches/` | hub heeft de Q; dienstpagina niet |
| alleen-douche-plaatsen | 669 / 0 | `/douche-plaatsen/` | pagina = het antwoord | MERGE INTO SERVICE PAGE | — |
| prijs-badkamerrenovatie | 476 / 0 | `/premie/` | deels (prijs ×4; "vanaf €6.000" = open klantvraag) | MERGE INTO SERVICE PAGE `/premie/` — prijsindicatie pas na klantbevestiging | — |
| hangtoilet-plaatsen | 193 / 0 | `/onze-toiletten/` | ja | MERGE | — |
| hoe-verloopt-renovatie | 166 / 1 | `/faq/` | hub-Q aanwezig | **FAQ HUB** `#hoe-verloopt` | proces-Q, past ook op `/over-ons/` |
| voordelen-badkamerrenovatie-door-ck | 154 / 1 | `/faq/` | nee | **MERGE INTO** `/over-ons/` | merk-overweging hoort bij over-ons |
| in-welke-regios | 84 / 0 | `/badkamer-renovatie-geel/` | ja (Kempen ×7, Turnhout, Mol, Westerlo…) | MERGE INTO SERVICE PAGE | juiste binding |
| showroom | 82 / 3 | `/faq/` | hub-Q aanwezig | FAQ HUB `#showroom` + link `/onze-projecten/` | antwoord "geen showroom, wel realisaties" |
| douche-aanpassen-senioren | 46 / 0 | `/seniorendouches/` | ja (pagina = antwoord) | MERGE | — |
| badkamer-inrichten | 40 / 0 | `/faq/` | hub-Q aanwezig | FAQ HUB | — |
| kleine-badkamer-renoveren | 31 / 0 | `/faq/` | hub-Q aanwezig | FAQ HUB (later: SUPPORT_WITHIN `/inloopdouche/`) | Sherlock-decision 83 "keep renoveren op deze FAQ" = fout gebonden |
| douchestoel-plaatsen | 4 / 0 | `/seniorendouches/` | hub-Q ja; pagina: zitje ×9 | MERGE | — |
| voordelen-douchetoilet | 1 / 0 | `/onze-toiletten/` | ja (douchetoilet ×8) | MERGE | Sherlock-decision 60 "keep" achterhaald |

Samenvatting: 11 MERGE (antwoord staat er), **5 SUPPORT_WITHIN_PAGE met ontbrekend antwoord** (zelf-inloopdouche, nadelen-zonder-breken, hoelang-duurt, lage-douchebak, senioren-leeftijd = samen 16.459 impr die nu op een pagina zonder het antwoord landen), **1 KEEP** (wasmachine), 4 FAQ HUB, 1 MERGE→over-ons, 0 RETIRE. De huidige blanket 7→`/faq/` is dus voor 4 URL's juist en voor 3 (wasmachine, hoelang, voordelen-ck) niet.

---

## 13. WHAT SHERLOCK CAN DO TODAY · WHAT CC HAD TO INFER · WHAT WATSON ACTUALLY BUILT

**WHAT SHERLOCK CAN DO TODAY (A, via MCP/UI op prod 0aa0c8b01)**
- GSC-evidence per pagina/query (`get_search_analytics`), lokale vraag als TYPE×CITY-segmentvoorstel (`suggest_tracking_segments`), segment aanmaken (`create_tracking_segment`).
- Page decisions berekenen, lezen en van status voorzien (`recompute_page_decisions`, `list_page_decisions`, `set_page_decision_status`) — per **topic**, met `covered_by_page_id`; 197 rijen voor CK.
- Briefs met H1/seo_title/content_angle/trust-feiten/SERP-afgeleide bloklijst (`generate_page_brief`, `compose_page_plan`).
- Render observeren (`observe_page_render`), lead-capture (`/api/leads/capture` → Kelvin), ontology met provenance (`update_client_ontology`).

**WHAT CC HAD TO INFER (MCS-1…9)**
- Realisatie-objecten (gemeente, regio, dienst, voor/na, probleem→oplossing) uit 35 gescrapete pagina's; locatie-surface-beslissingen; FAQ-per-URL-beslissingen; redirect-map; sectievolgorde; interne link-mesh; beeldkeuze; FAQ-selectie per pagina; toiletten-pagina; het "veilige douche"-territorium.
- Correctie van Sherlock-decisions die semantisch fout binden (Inloopdouche→galerij, Antwerpen→FAQ-toilet, locaties→/offerte/, keep op FAQ-URL's die gemerged worden).

**WHAT WATSON ACTUALLY BUILT**
- 9 pagina's op `preview.sherlockseo.com/ckservice` (6/9), **NOT ACCEPTED** (artifact 81: generieke copy, concurrentmerken als eigen product, brief-H1/meta 6/8).
- Launch-site = **0 % Watson**: Node-server + geportte reference + CC-gebouwde pagina's (CLIENT DELIVERY EXCEPTION artifact 94).
- Watson-theme bezit wél de primitieven die deze reconciliatie nodig heeft (CPT `realizations`, taxonomie `locations`, `project_types`, blok `realizations-gallery`) — nooit gevoed door Sherlock, niet voor CK gebruikt.

**Eerste breuk in de keten REAL DEMAND → DEMAND UNIT → PAGE/REALISATION → PAGE DECISION → COMPOSITION → MEDIA → BUILD → LINKS → TRACKING** (Geel als testcase):
1. DEMAND (A, ok): "badkamer renovatie geel" 99 impr enz.
2. DEMAND UNIT (A, ok maar niet uitgevoerd): TYPE×CITY Geel voorgesteld, niet aangemaakt.
3. CURRENT PAGE/REALISATION: pagina `/badkamer-renovatie-geel/` (site_page 10421) bestaat; realisatie Geel bestaat als crawl-rij zonder rol → **C** voor het realisatie-object.
4. PAGE DECISION: **geen decision voor Geel** — topic Geel excluded `off_niche:low_entity_distance`, `geo_coverage` leeg → **eerste breuk (B)**. De engine kan geen locatie-surface beslissen zolang de HQ-stad door de relevance-gate valt.
5. COMPOSITION: brief 44 bestaat met `local_info`-blok, maar zonder realisatie- of linkbinding (`internal_link_targets` 0, geen `page_decision_id`-kolom) → P.
6. DESIGN/MEDIA: geen asset-binding → C.
7. BUILD: Watson-primitief bestaat (B), niet aangesloten; launch-site = CC.
8. INTERNAL LINKS: geen producer → C.
9. TRACKING: A.

---

## VERTICAL SLICE — voorstel (nog niet uitgevoerd; geen pagina's gebouwd)

Slice = **Geel + realisatie `project-geel-bad-naar-douche` + dienst bad→douche/veilige douche**, exact langs de 9 stappen hierboven, zonder CC-synthese:
- Stap 2 (A): `list_tracking_segments` → indien geen Geel-segment: `create_tracking_segment` uit voorstel "TYPE×CITY — renovatie, badkamer, Geel" (+ badkamer/sanitair Geel). Verwacht: slaagt.
- Stap 4 (B→bewijs): `recompute_page_decisions` en aantonen dat er géén Geel-decision ontstaat; oorzaak = relevance-gate op locatie-topic + lege `geo_coverage`. Vullen van `geo_coverage` (klantfeit: Geel + 8 service areas) via `update_client_ontology` is A en toegestaan (ontology-correctie met provenance); daarna recompute → observeren of de engine dan wél een locatie-decision maakt. Dat is de eigenlijke test van de slice.
- Stap 5 (A/P): brief 44 opnieuw genereren ná de decision; controleren of `internal_link_targets` en een realisatie-verwijzing verschijnen (verwacht: niet → PLATFORM GAP CANDIDATE, geen lokale fix).
- Stap 6–8: alleen als 4–5 slagen; anders stopt de slice en wordt de breuk als evidence-artifact geregistreerd voor de orchestrator (geen nieuwe WI vanuit deze lane).
- Stap 9 (A): segment-evidence na launch.

Acceptatie van de slice = de Geel-pagina toont de Geel-realisatie en linkt naar `/veilige-douche/` **omdat Sherlock dat besliste en componeerde**, niet omdat CC het plaatste.

## PLATFORM GAP CANDIDATES uit deze reconciliatie (voor de orchestrator; geen WIs aangemaakt)

| Gap | Bewijs | Vermoedelijke owner |
|---|---|---|
| Geen realisatie-object (locatie × dienst × proof) in Sherlock; Watson-CPT ongevoed | §2, §7, §11 | geo lane (Slice B) / Watson |
| Relevance-gate sluit HQ-stad uit (`Geel off_niche`), `geo_coverage` ongebruikt door engine | §11, stap 4 | Slice A/B (#159-lane) |
| Page decisions per topic zonder URL/redirect-target; merges verwijzen naar page-id's | §10, MCS-5 | page-decision lane (#105) |
| `composition_briefs.page_decision_id` afwezig op prod; `internal_link_targets` nooit gevuld | §5 | composition lane (#161/#162), link graph #271 |
| Nieuwe briefs 48–58 voor concurrent-/retailmerken (Brico, Ideal Standard, Van Marcke) | §5 | competitor-entity filter (#162) |
| Brief 47 gebonden aan FAQ-URL i.p.v. opvolger `/premie/`; decisions "keep" op URL's die gemerged worden | §12 | page-decision lane |
| Locatie-decisions binden aan `/offerte/`, `/`, FAQ-toilet | §9 | page-decision lane |
