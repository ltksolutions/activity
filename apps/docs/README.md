# @activity/docs

Nextra projekt pre verejnú dokumentáciu projektu **activity**, nasadený na [docs.activity.sportup.sk](https://docs.activity.sportup.sk).

> Toto je app v rámci [activity monorepa](../../README.md). Pre prispievanie do dokumentácie pozri [CONTRIBUTING.md](../../CONTRIBUTING.md) v root-e repa.

## Stack

- **[Nextra 2](https://nextra.site)** — statický generátor dokumentácie
- **Next.js 14** — React framework
- **MDX** — Markdown s podporou JSX
- **TypeScript** — pre theme konfiguráciu

## Lokálny development

Z root-u monorepa:

```bash
npm install                 # nainštaluje workspaces
npm run dev --workspace=@activity/docs
```

Alebo priamo z `apps/docs/`:

```bash
cd apps/docs
npm install
npm run dev
```

Otvor [http://localhost:3000](http://localhost:3000).

## Štruktúra

```
apps/docs/
├── pages/                  ← MDX dokumentácia (zdroj pravdy)
│   ├── _meta.json          ← Navigácia v root-e
│   ├── index.mdx
│   ├── overview.mdx
│   ├── architecture.mdx
│   ├── domain-model.mdx
│   ├── mcp-servers.mdx
│   ├── sportup-sk-integration.mdx
│   ├── glossary.mdx
│   ├── features/           ← Featurové dokumenty
│   ├── workflows/          ← Per kategória používateľa
│   ├── acl/                ← ACL matice
│   ├── ops/                ← Prevádzka
│   └── ui/                 ← UI dokumenty
├── public/                 ← Statické assets (logo, favicon, OG image)
├── theme.config.tsx        ← Nextra theme konfigurácia
├── next.config.mjs         ← Next.js config
├── package.json
├── tsconfig.json
└── README.md
```

## Pridanie nového dokumentu

Detailne v [CONTRIBUTING.md](../../CONTRIBUTING.md). V skratke:

1. Vytvor `.mdx` súbor v príslušnom priečinku v `pages/`
2. Pridaj záznam do `_meta.json` v rovnakom priečinku
3. Otvor PR

## Pridanie novej sekcie (priečinka)

1. Vytvor priečinok v `pages/`
2. Vytvor `_meta.json` v ňom s usporiadaním stránok
3. Pridaj sekciu do root-ového `pages/_meta.json`

## Branding

**Logo, farby, typografia** sa preberajú z **Design manuálu pre sportup.sk** projekt.

### Pri implementácii

1. **Logo a ikony:**
   - SVG do `public/logo.svg`
   - `favicon.ico` do `public/`
   - OG image do `public/og-image.png`
   - V `theme.config.tsx` aktualizuj `logo` element

2. **Brand farba:**
   - V `theme.config.tsx` upraví `primaryHue` (HSL hue value, 0-360)
   - Default 165 (zelený-tyrkysový), uprav podľa Design manuálu

3. **Custom fonty:**
   - Defaultný font Nextra je Inter (cez Next.js fonts)
   - Pre custom font pridaj do `_app.mdx` alebo `next.config.mjs`

## Search

Vyhľadávanie je v MVP **vypnuté** (z dohody). Pri zapínaní:

1. V `theme.config.tsx` odstráň `search: { component: null }`
2. Voliteľne integrácia s [Algolia DocSearch](https://docsearch.algolia.com/) — vyžaduje aplikáciu o crawler
3. Alebo lokálny search cez Nextra default (FlexSearch) — funguje out-of-the-box

## Deployment

Deploy sa rieši cez Vercel z root-u monorepa. Pozri root [README.md](../../README.md) sekciu *Deployment*.

## Pre prispievateľov

Ak prispievaš obsah, **nemusíš si setupovať lokálny build**. Markdown stačí editovať priamo na GitHube cez webové UI a otvoriť PR. Vercel automaticky vygeneruje preview deployment pre každý PR, takže výslednú podobu uvidíš ešte pred merge.

Detaily v [CONTRIBUTING.md](../../CONTRIBUTING.md).
