<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
# @activity/web — marketing web pre activity.sportup.sk

Statický HTML/CSS/JS marketing web projektu **activity**, nasadený na [activity.sportup.sk](https://activity.sportup.sk).

> Toto je app v rámci [activity monorepa](../../README.md). Pre prispievanie pozri [CONTRIBUTING.md](../../CONTRIBUTING.md) v root-e repa.

## Stack

- **Statické HTML** — žiadny build framework
- **CSS** — vanilla, jeden `styles.css`
- **JavaScript** — vanilla, žiadne závislosti, jeden `script.js`
- **Vercel** — hosting

## Štruktúra

```
apps/web/
├── index.html              ← Domovská stránka
├── mentoring.html          ← Detail mentoringu (kľúčová stránka)
├── aktivity.html           ← Typy aktivít
├── courier.html            ← Komunikačný subsystém
├── pre-koho.html           ← Cieľové skupiny
├── priklady.html           ← Konkrétne scenáre
├── prepojenie.html         ← Vzťah k sportup.sk projektu
├── kontakt.html            ← Kontakt a odkazy
├── styles.css              ← Stylesheet
├── script.js               ← Vanilla JS (injekcia partials, mobile menu, active nav)
├── partials/               ← Re-use komponenty (header, footer)
│   ├── header.html
│   └── footer.html
├── assets/                 ← Statické assety (logá, obrázky — TBD)
├── vercel.json             ← Vercel deployment config
└── README.md               ← Tento súbor
```

## Princípy obsahu

Marketing web je iný žáner než dokumentácia. Princípy:

- **Konkrétny** — používame príbehy s menami (*"Tomáš a Peter"*), nie generické termíny
- **Vizuálny** — mockupy v UI štýle (faux-app komponenty v CSS), nie len text
- **Akčný** — každá stránka má linky na detail v dokumentácii
- **Prístupný** — žiadne *MCP, ACL, CSFLE* v hlavičkách, len v príslušných sekciách

Keď je technická presnosť dôležitá, **odkazujeme na dokumentáciu** (`docs.activity.sportup.sk`).

## Lokálny development

Web nemá build step — otvor súbory priamo v prehliadači, alebo použi jednoduchý dev server:

```bash
# Z apps/web/
python3 -m http.server 8080
# alebo
npx serve .
```

Otvor [http://localhost:8080](http://localhost:8080).

> ⚠️ **Pozor:** `script.js` načítava partials cez `fetch()`, ktorý funguje len cez HTTP server.
> Ak otvoríš `index.html` priamo zo súboru (`file://`), partials sa nenačítajú.

## Pridanie / úprava obsahu

### Úprava existujúcej stránky

Edituj príslušný `.html` súbor. Žiadny build, žiadny watcher — pri reload v prehliadači sa zmena prejaví.

### Pridanie novej stránky

1. Vytvor nový `.html` súbor (skopíruj štruktúru z existujúcej, napr. `kontakt.html`)
2. Pridaj záznam do `partials/header.html` (navigácia)
3. Pridaj záznam do `partials/footer.html` (ak chceš link aj v päte)
4. Otestuj lokálne

### Úprava hlavičky alebo päty

Edituj `partials/header.html` alebo `partials/footer.html` — zmena sa premietne na všetkých stránkach.

## Deployment

Nasadené na Vercel ako samostatný projekt s doménou `activity.sportup.sk`.

### Pridanie nového Vercel projektu

1. **Import Git Repository** → vyber `ltksolutions/Activity`
2. **Framework Preset:** Other (statický)
3. **Root Directory:** `apps/web`
4. **Build Command:** *(prázdne)*
5. **Output Directory:** `.` (root apps/web)
6. **Install Command:** *(prázdne)*

### Custom doména

V Vercel projekte → **Settings** → **Domains** → pridaj `activity.sportup.sk`.

DNS:
```
activity.sportup.sk  CNAME  cname.vercel-dns.com
```

TLS sa vystaví automaticky cez Let's Encrypt.

## Branding

Logo, farby a typografia sa preberajú z **Design manuálu pre sportup.sk** projekt
(activity je sub-projekt sportup.sk ekosystému).

### Pri implementácii doplň

| Súbor | Účel | Formát |
|---|---|---|
| `assets/logo.svg` | Hlavné logo (32px výška) | SVG |
| `assets/logo-mark.svg` | Skratená marka (favicon size) | SVG |
| `favicon.ico` | Browser tab ikona | ICO |
| `favicon-32x32.png` | Fallback favicon | PNG |
| `apple-touch-icon.png` | iOS home screen | PNG (180x180) |
| `og-image.png` | Open Graph náhľad | PNG (1200x630) |
| `site.webmanifest` | PWA manifest | JSON |

V `styles.css` upraví CSS premennú `--color-accent` (a varianty) podľa brand farby
z manuálu. Aktuálna placeholder hodnota je `#0f6e56`.

V `partials/header.html` v `<a class="site-logo">` nahraď textové logo SVG-čkom:

```html
<a href="/" class="site-logo">
  <img src="/assets/logo.svg" alt="activity" height="32" />
</a>
```

## Vzťah k ďalším apps

- **`apps/docs`** ([docs.activity.sportup.sk](https://docs.activity.sportup.sk)) — vývojárska dokumentácia v Nextra
- **`apps/platform-web`** (TBD, [activity.sportup.sk](https://activity.sportup.sk)) — vlastná web aplikácia platformy *(pozn.: marketing web je primárny obsah na activity.sportup.sk dokým neexistuje platform-web; po implementácii sa marketing presunie napríklad na `o.activity.sportup.sk` alebo zostane na home a platforma na `app.activity.sportup.sk`)*
