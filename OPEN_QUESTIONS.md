<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
# Otvorené otázky

> Toto je zoznam **rozhodnutí, ktoré sa v návrhovej fáze vedome nezavreli** a treba ich uzavrieť počas implementácie. Každá otázka má kontext, varianty riešenia, a ak má návrhová fáza preferenciu, je naznačená.
>
> Tento dokument **nie je TODO list pre features** — je to **decision queue** pre seniora developera.
> Pre featurový roadmap pozri [HANDOFF.md](./HANDOFF.md) sekciu *"Ako začať implementovať"*.

## Konvencia

Každá otázka je v jednej z troch kategórií:

- 🔴 **Blokujúca** — bez odpovede sa nedá začať implementácia
- 🟡 **Stredná** — dá sa začať, ale otázka sa raz musí zatvoriť
- 🟢 **Nízka** — má čas, môže sa rozhodnúť pred MVP launchom alebo neskôr

Po zatvorení otázky **napíš ADR-ku** (`apps/docs/pages/adr/00XX-<topic>.mdx`), ktorá zachytí rozhodnutie a dôvody.

---

## Infraštruktúra

### Q-001 🔴 Aký OIDC provider?

Architektúra predpokladá `auth.activity.sportup.sk` ako OIDC issuer. Treba zvoliť konkrétne riešenie:

- **(A) Keycloak** self-hosted v Cloud Run / k8s — full kontrola, open-source, ale prevádzka navyše
- **(B) Auth0** — managed, rýchle naštartovanie, ale platený nad istou hranicou MAU
- **(C) Logto** — open-source alternatíva Auth0, hosted aj self-hosted varianta
- **(D) Vlastná implementácia** — **NEODPORÚČANÉ**, tu sa veci ľahko pokazia

**Prefer:** (A) Keycloak ak má tím skúsenosti, inak (C) Logto.

### Q-002 🔴 MongoDB Atlas tier pre dev/staging/production?

Atlas má rôzne tiery, voľba ovplyvňuje features (M0 free nemá Atlas Search, M2/M5 áno):

- **Dev:** asi M0 free alebo M2 ($9/mes) — zatiaľ stačí
- **Staging:** M10 ($60/mes) — full feature set
- **Production:** M30+ s replication, backupom, audit logom

**Prefer:** Atlas tier-y skúmaj cez ich pricing kalkulačku, optimalizuj per-environment.

### Q-003 🔴 Redis hosting?

Redis Cloud, Upstash, Vercel KV, alebo self-hosted:

- **Upstash** — pay-per-request, dobrý pre nízky/stredný traffic
- **Redis Cloud** — managed s vyššími SLA
- **Vercel KV** — pohodlné ak používame Vercel pre frontend, ale obmedzený feature set
- **Self-hosted** v k8s — najlacnejšie pri vyššom traffic-u, ale prevádzka

**Prefer:** Upstash pre štart, prehodnotiť pri raste.

### Q-004 🟡 GitHub Actions vs. iný CI?

Default GitHub Actions, ale ak má tím preferenciu CircleCI / GitLab CI / Buildkite, ide to.

### Q-005 🟢 Monitoring stack?

Návrh predpokladá Grafana dashboardy. Konkrétne:

- **(A)** Grafana Cloud + Prometheus + Loki — managed
- **(B)** Self-hosted Grafana stack
- **(C)** Datadog / New Relic — vendor riešenie

**Prefer:** Začať s vendorom (Datadog free tier), prejsť na (A) ak náklady rastú.

### Q-006 🟢 CDN a DDoS pred Vercelom?

Návrh predpokladá Cloudflare. Vercel ale má vlastné edge / CDN. Otázka: pridáme Cloudflare ako extra layer (DDoS protection, WAF rules) alebo necháme len Vercel edge?

**Prefer:** Pridať Cloudflare po prvom DDoS incidente, nie predtým.

---

## Architektúra

### Q-007 🔴 Multi-tenant isolation: field-based alebo DB-per-tenant?

Návrh v dokumentácii predpokladá **field-based** scoping: každý dokument má `tenantId`, repository vrstva to vynucuje. To je rýchle a flexibilné, ale **jeden bug v repository → cross-tenant data leak**.

Alternatíva: **fyzicky oddelené databázy** per veľký tenant. Drahšie, ale tvrdé záruky.

Hybrid: malé tenants v zdielanej DB cez field, veľké tenants (zväzy, profesionálne kluby) vlastnú DB.

**Prefer:** field-based pre MVP. Hybrid prehodnotiť pri raste.

### Q-008 🔴 Schema validation: ručná Zod-to-JSONSchema synchronizácia, alebo code-gen?

Repo používa Zod schémy v aplikácii a JSON Schema validátory na MongoDB collection level. Tieto musia byť synchronizované.

- **(A)** Manuálne — riziko driftu medzi vrstvami
- **(B)** Zod → JSONSchema cez `zod-to-json-schema` package — automatika, treba to len commitnúť
- **(C)** Iný source of truth (TypeBox, JSONSchema first) — väčšia zmena

**Prefer:** (B) — `zod-to-json-schema` ako súčasť build-u packages/schemas.

### Q-009 🟡 Atlas Search vs. dedicated Elasticsearch / Meilisearch?

Návrh predpokladá Atlas Search (jednoduchosť, žiadny extra service). Pri raste sa môže ukázať, že **dedicated search** je potrebný.

**Prefer:** Atlas Search pre MVP, prehodnotiť pri load-e.

### Q-010 🟡 MCP servery: full Node.js process per server, alebo serverless functions?

Cloud Run / k8s podporuje obe varianty:

- **Process-per-server** — perzistentné, dobre pre WebSocket/SSE, predvídateľná latencia
- **Serverless** — škáluje na 0, lacnejšie pri nízkom traffic-u, ale cold start

**Prefer:** Process-per-server (Cloud Run min-instances=1) — kvôli SSE.

### Q-011 🟢 Zdielané utility code: jeden balík alebo per-server?

Currently navrhované: `packages/schemas` (zdielané schémy). Ale treba zvážiť aj:

- `packages/auth` — JWT validation, OIDC client
- `packages/db` — MongoDB connection, indexy helpers
- `packages/observability` — logging, tracing, metrics

Alebo nechať každý MCP server self-contained s duplicitným kódom (DRY vs ease of change).

**Prefer:** packages/schemas only pre MVP, ostatné per-server. Refaktorovať keď uvidíme duplicitu.

---

## Doménový model

### Q-012 🔴 Externí mentori: ako vyriešiť identity bez plného účtu?

Návrh hovorí *"lightweight identity"* (`Person.kind = 'external_lightweight'`), ale detail nie je úplne jasný:

- Má externý mentor email + poslať mu pozvánku do konkrétneho cyklu?
- Môže si neskôr "upgradnúť" účet na plný?
- Aký prístup má k UI — len read-only widget na sedeniach, alebo plnohodnotný cycle view?

**Prefer:** Email-based magic link, prístup len ku konkrétnemu cyklu, žiadne UI mimo to. Upgrade na full účet je separátny flow.

### Q-013 🟡 Polymorfné komentáre: indexy a query patterns

Návrh: `(activityType, activityId)` ako reference. Pri load-e treba mať dobrý plán pre:

- Top komentárov (čítané najčastejšie) → cache?
- Zobrazovanie pre konkrétnu aktivitu → kompozitný index `(tenantId, activityType, activityId, createdAt)` 
- Notifications na mention → separátny index `(mentionedPersonIds[], createdAt)` 

**Prefer:** indexy podľa Mongo `db.collection.explain()` výkonnostných meraní v dev.

### Q-014 🟡 Conversation retention override: per-conversation alebo per-message?

Návrh: `Conversation.retentionDays` umožňuje override per chat. Otvorené:

- Aplikuje sa na **všetky správy** v konverzácii, alebo len na novšie po nastavení?
- Pri zmene retencie hore/dole — recompute existujúcich správ?

**Prefer:** Aplikuje sa na všetky správy, recompute pri zmene cez background job.

### Q-015 🟢 Voľný text vs. štruktúra v `MentoringSession.summary`

Aktuálne summary je voľný text. Pre lepšie analytics by mohol byť štruktúrovaný:

- Akcie pre mentee (todo list)
- Pozorované silné stránky
- Pozorované oblasti pre rozvoj
- ...

Ale to robí formulár ťažší a kratšie sedenia jeden veľký šum.

**Prefer:** Voľný text pre MVP. Štruktúra v Phase 2 podľa user feedback.

---

## Bezpečnosť a privacy

### Q-016 🔴 CSFLE master key management

Návrh: Client-Side Field Level Encryption pre rodné číslo, lekárske diagnózy. Master key v AWS KMS. Otvorené:

- Aký AWS account, aký región KMS?
- Key rotation policy?
- Disaster recovery — ak stratíme master key, stratili sme všetky šifrované dáta. Ako to backupujeme?

**Prefer:** AWS KMS, eu-central-1, multi-region key, rotation každý rok, key backup do separátneho účtu.

### Q-017 🔴 E2E šifrovanie pre direct chat: Signal Protocol alebo vlastné?

Navrhnuté E2E pre direct, ale konkrétny protokol nie:

- **(A)** Signal Protocol (libsignal) — battle-tested, ale komplexný, treba understanding
- **(B)** Olm/Megolm (Matrix) — jednoduchší, dobrý pre group chat
- **(C)** Vlastné s libsodium — riskantné, ale flexibilné

**Prefer:** (A) Signal Protocol pre direct, (B) Olm pre group ak by sme E2E rozšírili (zatiaľ nie).

### Q-018 🟡 Rate limit storage: Redis sliding window — TTL strategie

Návrh: Redis Lua sliding window. Otvorené detaily:

- TTL pre counter keys (krátky → re-create overhead, dlhý → memory bloat)
- Dimenzionalita kľúčov (per IP + per token + per tenant — to je 3x storage)

**Prefer:** TTL = 2 × window_size, accept-header memory bloat za jednoduchosť.

### Q-019 🟡 Audit log: write strategy

Audit log je heavy-write. Synchronous write spomalí každú operáciu, async write riskuje stratu pri crash.

**Prefer:** Async write s retry queue (Redis), max 5 sec window pre stratu pri crash.

### Q-020 🟢 GDPR data export: synchronous alebo async?

Pre veľké tenants môže export trvať desiatky sekúnd až minúty. Synchronous response by timeoutol.

**Prefer:** Async generation s email notifikáciou na hotový download link (S3 signed URL, 24h validity).

---

## Frontend

### Q-021 🔴 State management v Next.js apps

Predvolené Next.js poskytuje server components + Suspense. Otázka pre client-side state:

- **(A)** Žiadny — len URL state + server fetches
- **(B)** TanStack Query (react-query) pre server cache + Zustand pre UI state
- **(C)** Redux Toolkit s RTK Query

**Prefer:** (B) — react-query je dnes default pre server state, Zustand pre UI je minimal.

### Q-022 🟡 Component library / design system

Dokumentácia (`ui/design-principles.mdx`) hovorí Radix UI primitives + Tailwind. Otázka:

- Použiť **shadcn/ui** (ready-made Radix + Tailwind komponenty) alebo postaviť vlastný `packages/ui`?

**Prefer:** shadcn/ui ako base, custom rozšírenia v `packages/ui` per potreba.

### Q-023 🟡 i18n knižnica: next-intl alebo iné?

Návrh: `next-intl`. Konkurencia: `react-i18next`, `lingui`.

**Prefer:** next-intl je default v Next.js community, žiadny dôvod meniť.

### Q-024 🟢 Mobile aplikácia: React Native, alebo PWA?

V návrhu sme to úplne neriešili. PWA pre MVP stačí, neskôr môže byť potreba native.

**Prefer:** PWA pre MVP. Native ako budúca téma.

---

## Procesy

### Q-025 🟡 Branch strategy: GitHub Flow alebo GitFlow?

CONTRIBUTING.md predpokladá feature branches + main. Či bude staging branch alebo nie, je na tebe.

**Prefer:** GitHub Flow (main + feature branches), bez staging branch. Staging environment z `main` continuous deploy.

### Q-026 🟡 PR review policy

CODEOWNERS automaticky tagne reviewer-ov, ale **počet schválení**, **squash vs merge**, **branch protection rules** treba nastaviť v GitHub Settings.

**Prefer:** 1 schválenie od ownera, squash merge, branch protection na main (no direct push, require PR).

### Q-027 🟢 Versioning a release notes

Pri prvom production deploy treba začať s versioning-om. SemVer? CalVer? Ako vyzerajú release notes?

**Prefer:** SemVer pre packages, CalVer pre apps (`v2026.04.29`). Release notes auto-generated z conventional commits cez `changesets`.

---

## Vyplnené otázky

> Pri zatvorení každej otázky **napíš ADR-ku**, presunieš ju z tohto dokumentu sem nižšie, a v ADR linkneš pôvodné Q-číslo.

*(Zatiaľ žiadna)*

---

## Ako pridať novú otázku

Ak narazíš na rozhodnutie, ktoré nepatrí do jedného PR-u (lebo je príliš veľké) ani do ADR-ky (lebo ešte nie je rozhodnuté), pridaj ju sem v rovnakom formáte:

```markdown
### Q-028 🔴 Krátky popis otázky

Kontext (1-3 vety) — prečo otázka existuje.

- **(A)** Prvá varianta — pros/cons
- **(B)** Druhá varianta — pros/cons

**Prefer:** ak má niekto odhad / preferenciu (voliteľné).
```

A inkrementuj číslo. Po zatvorení (cez ADR-ku) presuň do *Vyplnené otázky*.
