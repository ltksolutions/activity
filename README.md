<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
# activity

**Platforma pre evidenciu aktivít, mentoring a komunikáciu v slovenskom športe** — športovci, tréneri, rozhodcovia, lekári, fanúšikovia a podporovatelia v jednom systéme.

[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL--1.2-blue.svg)](LICENSE)
[![License: CC-BY-4.0](https://img.shields.io/badge/Docs_License-CC--BY--4.0-lightgrey.svg)](LICENSE-DOCS)
[![REUSE status](https://api.reuse.software/badge/github.com/ltksolutions/activity)](https://api.reuse.software/info/github.com/ltksolutions/activity)
[![Status: MVP](https://img.shields.io/badge/Status-MVP-orange.svg)]()
[![Slovak](https://img.shields.io/badge/Lang-Slovak-blue.svg)]()

Tento repozitár je **monorepo** obsahujúci všetky aplikácie a balíky tvoriace platformu activity.

## Vzťah k projektu sportup.sk

**activity** je klient projektu [sportup.sk](https://github.com/ltksolutions/sportup.sk) — využíva jeho registre osôb a organizácií ako autoritatívny zdroj.

| Projekt | Doména | Repo | Zodpovednosť |
|---|---|---|---|
| [sportup.sk](https://github.com/ltksolutions/sportup.sk) | `sportup.sk` | `ltksolutions/sportup.sk` | Registre osôb a organizácií, číselníky |
| **activity** (tento repo) | `activity.sportup.sk` | `ltksolutions/activity` | Aktivity, mentoring, komunikácia |

Detaily integrácie v [Integrácia s sportup.sk](https://docs.activity.sportup.sk/sportup-sk-integration).

## Stav

🚧 **MVP fáza** — aktívny vývoj.

Aktuálne hotové:

- ✅ **Marketing web** ([activity.sportup.sk](https://activity.sportup.sk)) — statický web s prehľadom projektu
- ✅ **Dokumentácia** — kompletný technický a produktový popis systému ([docs.activity.sportup.sk](https://docs.activity.sportup.sk))
- ⏳ Backend (MCP servery) — TBD
- ⏳ Web aplikácia ([app.activity.sportup.sk](https://app.activity.sportup.sk)) — TBD
- ⏳ Admin aplikácia ([admin.activity.sportup.sk](https://admin.activity.sportup.sk)) — TBD
- ⏳ Zdielané schémy package — TBD

## Pre senior vývojárov, ktorí preberajú projekt

Ak preberáš projekt do implementačnej fázy, **začni tu**:

1. **[HANDOFF.md](./HANDOFF.md)** — prehľad stavu, čo je hotové, čo TBD, fázy implementácie
2. **[OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md)** — explicitný zoznam ~27 otvorených rozhodnutí, ktoré treba uzavrieť
3. **[ADR (Architecture Decision Records)](https://docs.activity.sportup.sk/adr)** — 12 dokumentov, ktoré zachytávajú prečo sú veci tak ako sú (stack, doménové vzory, security)
4. **[Dokumentácia](https://docs.activity.sportup.sk)** — kompletný popis systému

Tieto štyri zdroje pokryjú 90% otázok, ktoré budeš mať pred prvým commitom.



```
activity/
├── apps/
│   ├── web/                 ← Marketing web (activity.sportup.sk) — statický HTML
│   ├── docs/                ← Vývojárska dokumentácia (docs.activity.sportup.sk, Nextra)
│   ├── platform-web/        ← (TBD) Web aplikácia (app.activity.sportup.sk)
│   ├── platform-admin/      ← (TBD) Admin aplikácia (admin.activity.sportup.sk)
│   ├── registry-mcp/        ← (TBD) MCP server: lokálny mirror sportup.sk + naše rozšírenia
│   ├── activity-mcp/        ← (TBD) MCP server: aktivity, mentoring, komentáre
│   └── courier-mcp/         ← (TBD) MCP server: chat a komunikácia
├── packages/
│   └── schemas/             ← (TBD) @activity/schemas — zdielané Zod schémy
├── .github/                 ← GitHub konfigurácia (PR templates, CODEOWNERS, ...)
├── package.json             ← Root workspace config
├── README.md                ← Tento súbor
├── CONTRIBUTING.md          ← Pokyny pre prispievateľov
├── LICENSE                  ← EUPL-1.2 (zdrojový kód)
├── LICENSE-DOCS             ← CC-BY-4.0 (dokumentácia, marketing, brand)
├── LICENSES/                ← REUSE Specification — plné texty licencií
├── REUSE.toml               ← REUSE — anotácie pre binárne súbory
└── CITATION.cff             ← Citačné údaje (academic / public sector)
```

## Začni tu

### Pre čítanie dokumentácie

📖 [docs.activity.sportup.sk](https://docs.activity.sportup.sk) — verejná dokumentácia. **Žiadne prihlásenie.** Začni s [prehľadom](https://docs.activity.sportup.sk/overview).

### Pre kontribúciu

📝 Pozri [CONTRIBUTING.md](./CONTRIBUTING.md) — pokyny pre prispievateľov.

### Pre lokálny development

```bash
git clone https://github.com/ltksolutions/activity.git
cd activity
npm install
```

Spustenie konkrétnej aplikácie:

```bash
npm run dev:docs    # Dokumentácia (Nextra) na http://localhost:3000
npm run dev:web     # Marketing web (statický) na http://localhost:8080
```

## Technologický stack

- **MongoDB Atlas** — primárna databáza (native driver + Zod)
- **Node.js + Fastify** — backend MCP servery
- **Next.js 15** — frontend (web aplikácia, admin)
- **Nextra** — generátor dokumentácie
- **MCP (Model Context Protocol)** — primárne API rozhranie
- **Redis** — pub/sub, cache, rate limiting
- **TypeScript** — naprieč celým stackom
- **Vercel** — hosting Next.js apps
- **Cloud Run / k8s** — hosting MCP serverov
- **Cloudflare** — CDN a DDoS ochrana
- **Caddy** — on-demand TLS pre custom domény organizácií

Detail v [Architektúra](https://docs.activity.sportup.sk/architecture) sekcii dokumentácie.

## Deployment

### apps/web → activity.sportup.sk

Vercel projekt (statický web bez frameworku):

- **Framework Preset:** Other
- **Root Directory:** `apps/web`
- **Build Command:** *(prázdne)*
- **Output Directory:** `.`

DNS: `activity.sportup.sk CNAME cname.vercel-dns.com`

### apps/docs → docs.activity.sportup.sk

Vercel projekt napojený na tento repo:

- **Framework Preset:** Next.js
- **Root Directory:** `apps/docs`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install` (z root-u, monorepo)

DNS: `docs.activity.sportup.sk CNAME cname.vercel-dns.com`

### Ostatné apps

TBD — postupne pribudnú s implementáciou.

## Licencia

Projekt používa **dual licenčný model** rovnako ako sister projekt [sportup.sk](https://github.com/ltksolutions/sportup.sk):

| Časť | Licencia | Pokrytie |
|---|---|---|
| **Zdrojový kód** (TS/TSX/CSS/JS/Python) | [**EUPL-1.2**](./LICENSE) | `apps/*/src`, shared packages, build tools |
| **Dokumentácia, brand, marketing** | [**CC-BY-4.0**](./LICENSE-DOCS) | `apps/docs/`, `apps/web/`, `branding-source/`, `*.md` |

Projekt je **REUSE-compliant** ([REUSE Specification 3.3](https://reuse.software/spec/)) — každý súbor má buď SPDX header, alebo je pokrytý cez [`REUSE.toml`](./REUSE.toml). Verifikácia:

```bash
pipx install reuse  # alebo: pip install --user reuse
reuse lint
```

Compliance je **automaticky kontrolovaná pri každom push a pull request** — pozri [`.github/workflows/reuse.yml`](./.github/workflows/reuse.yml). REUSE je odporúčaný prístup [EÚ Joinup](https://joinup.ec.europa.eu/) pre softvér verejného sektora.

**Prečo EUPL?** EUPL-1.2 je oficiálna open-source licencia Európskej únie, dostupná v 23 jazykoch vrátane slovenčiny, copyleft kompatibilná s GPL/AGPL/MPL, navrhnutá pre verejný sektor. Pozri [ADR-014](https://docs.activity.sportup.sk/adr/0014-licensing-eupl-reuse).

## Kontakt a podpora

Otázky a issues priamo v tomto repozitári cez GitHub Issues. Pre obsah dokumentácie použij label `docs`, pre kód `code`.
