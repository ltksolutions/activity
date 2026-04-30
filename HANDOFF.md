# Handoff dokument

> Toto je vstupný bod pre senior developera, ktorý preberá projekt **activity** do implementačnej fázy. Cieľom dokumentu je dať za 30 minút prehľad o tom, čo je hotové, čo je rozhodnuté, čo je otvorené, a kde sa s tým ďalej pracuje.

## V skratke

**activity** je platforma pre evidenciu aktivít, mentoring a komunikáciu v slovenskom športe. Stavia ako *klient* nad projektom [sportup.sk](https://github.com/ltksolutions/sportup.sk), ktorý poskytuje registre osôb a organizácií.

Aktuálny stav: **kompletná návrhová a dokumentačná fáza** je za nami. Implementácia (kód) sa zatiaľ **nezačala** — ten krok preberáš ty.

## Dva linky, ktoré stačia na začiatok

1. **[docs.activity.sportup.sk](https://docs.activity.sportup.sk)** — kompletná technická a produktová dokumentácia (~10 000 riadkov, 26 dokumentov)
2. **[activity.sportup.sk](https://activity.sportup.sk)** — marketing web s vysvetleniami pre koncových používateľov

Repo: **[github.com/ltksolutions/activity](https://github.com/ltksolutions/activity)** (kde si práve teraz)

## Čo je hotové

| Vrstva | Stav | Kde to nájdeš |
|---|---|---|
| Doménový model | ✅ Hotové | [docs.activity.sportup.sk/domain-model](https://docs.activity.sportup.sk/domain-model) |
| Architektúra (3 MCP servery) | ✅ Návrh | [docs.activity.sportup.sk/architecture](https://docs.activity.sportup.sk/architecture) |
| API špecifikácia (MCP tools, resources) | ✅ Návrh | [docs.activity.sportup.sk/mcp-servers](https://docs.activity.sportup.sk/mcp-servers) |
| ACL matice (Courier, komentáre) | ✅ Návrh | [docs.activity.sportup.sk/acl](https://docs.activity.sportup.sk/acl/matrix-comments) |
| Workflow per kategória používateľa | ✅ Hotové | [docs.activity.sportup.sk/workflows](https://docs.activity.sportup.sk/workflows/athlete) |
| Featurové dokumenty (mentoring, courier, ...) | ✅ Hotové | [docs.activity.sportup.sk/features](https://docs.activity.sportup.sk/features/mentoring) |
| Operácie (deployment, retencia, GDPR) | ✅ Návrh | [docs.activity.sportup.sk/ops](https://docs.activity.sportup.sk/ops/deployment) |
| Integrácia s sportup.sk | ✅ Návrh | [docs.activity.sportup.sk/sportup-sk-integration](https://docs.activity.sportup.sk/sportup-sk-integration) |
| Marketing web | ✅ Live | [activity.sportup.sk](https://activity.sportup.sk) |
| Branding (logo, farby, favicon, OG) | ✅ Hotové | `apps/web/assets/`, `apps/docs/public/` |
| **Architecture Decision Records (ADR)** | ✅ Hotové | [docs.activity.sportup.sk/adr](https://docs.activity.sportup.sk/adr) |
| **Otvorené otázky pre seniora** | ✅ Hotové | [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) |

## Čo nie je hotové (preberáš ty)

| Komponent | Subdoména | Zodpovednosť |
|---|---|---|
| `registry-mcp` | `registry-mcp.activity.sportup.sk` | Lokálny mirror sportup.sk + naše rozšírenia |
| `activity-mcp` | `activity-mcp.activity.sportup.sk` | Aktivity, mentoring, polymorfné komentáre |
| `courier-mcp` | `courier-mcp.activity.sportup.sk` | Chat (direct, group, broadcast) |
| Web aplikácia | `app.activity.sportup.sk` | Hlavný klient platformy (Next.js) |
| Admin aplikácia | `admin.activity.sportup.sk` | Správa organizácií, moderation |
| OIDC provider | `auth.activity.sportup.sk` | Autentifikácia (existujúce riešenie ako Keycloak alebo vlastné) |
| API gateway | `api.activity.sportup.sk` | REST nadstavba nad MCP pre HTTP klientov |
| Zdielané schémy | `packages/schemas` | Zod schémy doménových modelov |
| MongoDB Atlas cluster | – | DB infraštruktúra |
| Redis (pub/sub, cache) | – | Real-time delivery, rate limiting |
| CI/CD | – | GitHub Actions, deployment pipeline |

## Stack rozhodnutia (čo je už zafixované)

Tieto rozhodnutia padli, otvorenie ich znova by stratilo prácu. Sú podložené v ADR-kách:

- **MongoDB Atlas** + native driver + **Zod** schémy + **JSON Schema** validátory na collection level — [ADR-001](https://docs.activity.sportup.sk/adr/0001-database-mongodb), [ADR-002](https://docs.activity.sportup.sk/adr/0002-no-orm-zod-only)
- **Node.js + Fastify** pre MCP servery, polyglot deployment (3 servery, nie monolit) — [ADR-003](https://docs.activity.sportup.sk/adr/0003-mcp-polyglot)
- **Next.js 15** pre frontend aplikácie, **Vercel** hosting — [ADR-004](https://docs.activity.sportup.sk/adr/0004-frontend-stack)
- **MCP (Model Context Protocol)** ako primárne API rozhranie, REST gateway ako proxy — [ADR-005](https://docs.activity.sportup.sk/adr/0005-mcp-as-primary-api)
- **Polymorfné komentáre** cez `(activityType, activityId)` pre všetky typy aktivít — [ADR-006](https://docs.activity.sportup.sk/adr/0006-polymorphic-comments)
- **MentoringCycle** ako kontainer (nie aktivita), **MentoringSession** ako aktivita pod ním — [ADR-007](https://docs.activity.sportup.sk/adr/0007-mentoring-cycle-vs-session)
- **End-to-end šifrovanie** len pre `direct` chat, server-side encryption pre `group` a `broadcast` — [ADR-008](https://docs.activity.sportup.sk/adr/0008-e2e-only-direct)
- **Rodičovský proxy** ako separátne `ConversationParticipant` účastníctvo s `participantType: 'proxy_for_minor'` — [ADR-009](https://docs.activity.sportup.sk/adr/0009-parental-proxy)
- **Hybrid mirror** s sportup.sk: identitné polia mirror, aplikačné polia lokálne — [ADR-010](https://docs.activity.sportup.sk/adr/0010-sportup-mirror)
- **SSE + Redis Pub/Sub** pre real-time delivery (nie WebSocket, nie Change Streams) — [ADR-011](https://docs.activity.sportup.sk/adr/0011-sse-realtime)
- **Vercel** zostáva pre Next.js apps, nie ideme na Google ani inú cloud — [ADR-012](https://docs.activity.sportup.sk/adr/0012-vercel-stays)

## Čo ja **neviem**, čo musíš ty

Nie všetko sa dalo dotiahnuť do konca v návrhovej fáze. Nasledujúce sú **otvorené otázky**, ktoré som vedome nezavrela a treba ich uzavrieť pri implementácii:

➡️ Pozri **[OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md)** pre kompletný zoznam (~25 položiek rozdelených do kategórií).

V krátkosti, najpálčivejšie:

- **Aký OIDC provider** (Keycloak self-hosted? Auth0? Custom?)
- **Akú MongoDB tier** v Atlas-e pre MVP a production
- **Schema validation strategy** — keep Zod-to-JSONSchema in sync manuálne, alebo cez code-gen?
- **Multi-tenant isolation** — strict per-tenant DB, alebo logical scoping cez `tenantId` field? (default v dokumentácii je field, ale niektoré scenáre to môžu vyžadovať tvrdšie)
- **CI/CD platforma** — GitHub Actions je default, ale ak chceš niečo iné, ide to

## Ako začať implementovať

Toto je môj návrh poradia, pre teba aj pre tím:

### Fáza 0: Discovery (1-2 týždne)

1. Prejdi celú dokumentáciu na `docs.activity.sportup.sk`
2. Prečítaj **všetky ADR-ky** v `apps/docs/pages/adr/`
3. Prejdi **[OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md)** a zatvor tie, ktoré sú blokujúce pre Fázu 1
4. Naplánuj infrastruktúru (MongoDB Atlas account, Redis Cloud / Upstash, Vercel team setup)
5. Pripravte ADR-ky pre rozhodnutia, ktoré spravíš (pokračujte v číslovaní 13, 14, ...)

### Fáza 1: Foundation (2-4 týždne)

1. **`packages/schemas`** — extrahovať Zod schémy z dokumentácie do TypeScript packagu
2. **`apps/registry-mcp`** — najprv tento, lebo activity-mcp a courier-mcp nad ním stoja
3. Príprava sportup.sk integrácie (webhook listener, mirror sync)
4. CI/CD pipeline, dev/staging environments

### Fáza 2: Core features (4-8 týždňov)

1. **`apps/activity-mcp`** — aktivity, mentoring (najprioritnejší feature pre marketing)
2. **`apps/courier-mcp`** — chat
3. **`apps/platform-web`** (Next.js) — minimálne use case-y, ktoré odprezentujú aplikáciu

### Fáza 3: Production-ready (4-6 týždňov)

1. Admin app, OIDC integrácia
2. Atlas Search index-y, retencia, GDPR endpointy
3. Load testing, security audit, accessibility audit
4. Production deploy

## Komunikácia s pôvodným tímom

Tento projekt mal pôvodne dokumentačnú fázu so **mnou (Claude)** ako sparing partnerom Jana Letka. Návrhy a rozhodnutia, ktoré sú v dokumentácii, vznikli v dialógu medzi nami dvoma — teda **niektoré budú treba ešte doladit s Janom alebo skontrolovať voči realite tímu**.

Pre otázky:
- **Produktové / doménové** (*"prečo presne takto sa rieši mentoring?"*) → kontaktuj Jana, prípadne pozri ADR
- **Implementačné** (*"ako toto najlepšie nakódovať?"*) → tvoja zodpovednosť, ale rád ťa Jan podporí
- **Otázky o pôvodnom dialógu / kontexte** → Jan má prístup k transkriptom rozhovorov

## Ďalšie dokumenty v tomto repe

| Súbor | Účel |
|---|---|
| [README.md](./README.md) | Obecný prehľad projektu, štruktúra repa |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Pokyny pre prispievateľov (najmä do dokumentácie) |
| **[HANDOFF.md](./HANDOFF.md)** | Tento dokument |
| **[OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md)** | Explicitný zoznam otvorených otázok |
| `apps/docs/pages/adr/` | Architecture Decision Records (15 ADR-iek) |
| `apps/docs/pages/` | Kompletná dokumentácia (deployne na docs.activity.sportup.sk) |
| `apps/web/` | Marketing web (deployne na activity.sportup.sk) |
| [LICENSE](./LICENSE) | MIT |

## Zoznam ľudí

V `.github/CODEOWNERS` sú aktuálne všade `@<placeholder>` — tieto treba nahradiť reálnymi GitHub usernamami pri prebierke. To umožní GitHub auto-tagging reviewerov pri PR-och.

## Posledné slovo

Dokumentácia je **návrh**, nie zákon. Ak narazíš na rozhodnutie, ktoré nedáva zmysel v reálnej implementácii, **otvor o tom diskusiu** (GitHub Issue, ADR pre overrid). Niektoré rozhodnutia môžu byť pekné na papieri ale ťažké v praxi.

Naopak, niektoré rozhodnutia sú **úmyselne tvrdé** (napríklad ACL pre lekárske záznamy, retencia, GDPR — tieto majú zákonné/etické dôvody) a tie meniť **nie**.

ADR-ky sú dobrý kompromis — keď meníš rozhodnutie, napíš novú ADR-ku, ktorá *supersede-uje* starú. Tak vidno, že rozhodnutie sa vedome zmenilo a prečo.

---

Veľa šťastia.
