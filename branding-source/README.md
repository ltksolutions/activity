# branding-source

> **Source of truth pre brand v2** — interaktívne HTML dokumenty s definíciami loga, farieb, typografie a ikon. Tieto súbory pochádzajú z dizajnovej fázy a slúžia ako **autoritatívny zdroj** pre regeneráciu brand assetov v `apps/web/assets/` a `apps/docs/public/`.

## Súbory

| Súbor | Obsah | Čo z toho vzniká |
|---|---|---|
| [`activity-logo.html`](./activity-logo.html) | Všetky varianty loga (primary, dark, mono, on-blue, mono-white, symbol-only) v interaktívnom previewe + sekcia *"08 SVG export"* s kanonickým SVG kódom | `apps/web/assets/logo.svg`, `logo-dark.svg`, `logo-mono.svg`, `logo-mono-white.svg`, `logo-on-blue.svg`, `logo-mark.svg`, `logo-mark-dark.svg` |
| [`activity-brand-manual.html`](./activity-brand-manual.html) | Kompletný 8-stránkový brand manuál (A4, exportovateľný do PDF): logo, farby, typografia, app ikony, digitálne aplikácie | Slúži ako referenčný dokument pre dizajnérov a vývojárov; je zdrojom pre [`apps/docs/pages/ui/brand`](../apps/docs/pages/ui/brand) |
| [`activity-icons.html`](./activity-icons.html) | 32 UI ikon na 24×24 mriežke (stroke 1.8px, round caps) v 4 kategóriách: Communication, People, Activity & Sport, Navigation & UI | TBD: `packages/ui/icons/` keď bude existovať. Zatiaľ slúžia ako referencia pre Lucide selection alebo custom SVG icon set |
| [`BRAND-MANUAL-README.md`](./BRAND-MANUAL-README.md) | Pôvodný README od dizajnového tímu (originál) | Historický záznam — needited |

## Ako tieto súbory čítať

Otvor v prehliadači:

```bash
open branding-source/activity-logo.html
open branding-source/activity-brand-manual.html
open branding-source/activity-icons.html
```

Súbory sú **statické HTML s inline CSS** — žiadne build dependencies, žiadne externé fonty (okrem Google Fonts). Otvoria sa v ľubovoľnom prehliadači.

V `activity-logo.html` je v sekcii **"08 SVG export"** kanonický SVG kód každej logo varianty s tlačidlom *"Kopírovať SVG"* — to je presný zdroj, z ktorého sú generované súbory v `apps/web/assets/*.svg`.

V `activity-brand-manual.html` je tlačidlo *"Exportovať PDF"* — vyrenderuje sa A4 PDF s kompletným brand manuálom (Cmd+P → Paper A4 → Margins None → Background graphics ON → Save as PDF).

## Workflow pri zmene brandu

1. **Diskusia s dizajnérom** o zmene (farba, layout, typografia)
2. **Update HTML súboru** v `branding-source/` — napr. zmena hex farby v `activity-brand-manual.html` + `activity-logo.html`
3. **Spusti regen skript:**
   ```bash
   python3 tools/build-brand-assets.py
   ```
   Vygeneruje všetky PNG/ICO assety v `apps/web/assets/` + skopíruje ich do `apps/docs/public/`.
4. **Update SVG súborov ručne** v `apps/web/assets/*.svg` (skopírovať z aktualizovaného `activity-logo.html` sekcie *"08 SVG export"*)
5. **Update farieb/tokenov** v `apps/web/styles.css` a `apps/docs/theme.config.tsx` ak je zmenená paleta
6. **Update brand dokumentácie** v `apps/docs/pages/ui/brand.mdx`
7. **Napíš novú ADR-ku** ak je zmena podstatná (preferred ak nie je kozmetická). Pozri ADR-013 brand v2 ako šablónu.
8. **Lokálne overenie** — otvor `apps/web/index.html`, over v Chrome DevTools že favicon, theme-color, logo sa zobrazujú správne. Pre docs `cd apps/docs && pnpm dev`.

## Vzťah k ostatným súborom v repe

```
branding-source/                    ← TU (source of truth)
  ├── activity-logo.html            ← SVG kód v "08 SVG export"
  ├── activity-brand-manual.html    ← farby, typografia, layout
  ├── activity-icons.html           ← 32 UI ikon
  └── BRAND-MANUAL-README.md        ← pôvodný readme

tools/
  └── build-brand-assets.py         ← regen skript (PIL natívne)

apps/web/
  ├── styles.css                    ← --sk-blue, --sk-red, --ink, --paper tokeny
  └── assets/                       ← finálne SVG/PNG/ICO/manifest

apps/docs/
  ├── theme.config.tsx              ← Nextra config s primaryHue 225° (SK Blue)
  ├── pages/ui/brand.mdx            ← brand manuál v Nextra docs (verejný)
  └── public/                       ← kópie brand assetov pre docs subdomain
```

Brand manual v Nextra (`apps/docs/pages/ui/brand.mdx`) je **derived view** týchto HTML súborov — slúži ako verejná dokumentácia pre vývojárov, ktorí stavajú frontend aplikácie nad activity. HTML v `branding-source/` zostáva ako **technický zdroj** pre regen.

## Verzie

| Verzia | Dátum | Zmena | ADR |
|---|---|---|---|
| v1.0 | 2026-04 | Pôvodný brand: navy + slovak red, AU monogram | — |
| v2.0 | 2026-05 | Prerod na SK Blue + SK Red + Chat Stack mark + Albert Sans/Geist | [ADR-013](../apps/docs/pages/adr/0013-brand-v2) |
