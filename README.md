# activity

**Platforma pre evidenciu aktivít, mentoring a komunikáciu v slovenskom športe** — športovci, tréneri, rozhodcovia, lekári, fanúšikovia a podporovatelia v jednom systéme.

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

- ✅ **Dokumentácia** — kompletný technický a produktový popis systému ([docs.activity.sportup.sk](https://docs.activity.sportup.sk))
- ⏳ Backend (MCP servery) — TBD
- ⏳ Web aplikácia ([activity.sportup.sk](https://activity.sportup.sk)) — TBD
- ⏳ Admin aplikácia ([admin.activity.sportup.sk](https://admin.activity.sportup.sk)) — TBD
- ⏳ Zdielané schémy package — TBD

## Štruktúra repozitára

```
activity/
├── apps/
│   ├── docs/                ← Vývojárska dokumentácia (Nextra, docs.activity.sportup.sk)
│   ├── platform-web/        ← (TBD) Web aplikácia (activity.sportup.sk)
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
└── LICENSE                  ← MIT
```

## Začni tu

### Pre čítanie dokumentácie

📖 [docs.activity.sportup.sk](https://docs.activity.sportup.sk) — verejná dokumentácia. **Žiadne prihlásenie.** Začni s [prehľadom](https://docs.activity.sportup.sk/overview).

### Pre kontribúciu

📝 Pozri [CONTRIBUTING.md](./CONTRIBUTING.md) — pokyny pre prispievateľov.

### Pre lokálny development dokumentácie

```bash
git clone https://github.com/ltksolutions/activity.git
cd activity
npm install
npm run dev:docs
```

Otvor [http://localhost:3000](http://localhost:3000).

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

### apps/docs → docs.activity.sportup.sk

Vercel projekt napojený na tento repo:

- **Framework preset:** Next.js
- **Root directory:** `apps/docs`
- **Build command:** `npm run build`
- **Output directory:** `.next`
- **Install command:** `npm install` (z root-u, monorepo)

Custom doména `docs.activity.sportup.sk` nakonfigurovaná v Vercel:

```
docs.activity.sportup.sk  CNAME  cname.vercel-dns.com
```

### Ostatné apps

TBD — postupne pribudnú s implementáciou.

## Licencia

MIT — pozri [LICENSE](./LICENSE).

## Kontakt a podpora

Otázky a issues priamo v tomto repozitári cez GitHub Issues. Pre obsah dokumentácie použij label `docs`, pre kód `code`.
