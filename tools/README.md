# tools/

> Pomocné skripty pre údržbu projektu activity. Nie sú súčasťou build pipeline žiadnej apps — spúšťajú sa ručne pri údržbe.

## Skripty

### `build-brand-assets.py`

**Účel:** Regenerácia všetkých rastrových brand assetov (PNG, ICO) v `apps/web/assets/` a kópií v `apps/docs/public/`.

**Kedy spustiť:**
- Po zmene farieb v `branding-source/activity-brand-manual.html`
- Po zmene Chat Stack layoutu
- Po zmene OG image tagline / claim
- Pri prerenderovaní pre kontrolu kvality

**Spustenie:**

```bash
# Z root-u repa
python3 tools/build-brand-assets.py
```

**Závislosti:**

```bash
# Macový built-in Python 3.9+ (/usr/bin/python3)
pip install --user Pillow fonttools brotli
```

**Čo vygeneruje (19 súborov):**

```
apps/web/assets/
├── logo-mark-256.png        ← mark only PNG raster
├── logo-mark-512.png
├── logo-mark-1024.png
├── favicon-16x16.png        ← favicon set
├── favicon-32x32.png
├── favicon-192x192.png
├── favicon-512x512.png
├── favicon.ico              ← multi-res ICO (16/32/48)
├── apple-touch-icon.png     ← 180×180 paper bg
├── icon-maskable-192.png    ← Android adaptive (biely Chat Stack na SK Blue)
├── icon-maskable-512.png
└── og-image.png             ← 1200×630 social share

apps/web/
└── favicon.ico              ← root copy (legacy odkazy)

apps/docs/public/
└── (kópie 11 brand assetov pre Nextra)
```

**Čo NEgeneruje:**
- **SVG súbory** — `logo.svg`, `logo-dark.svg`, `logo-mark.svg`, `favicon.svg`, etc. sú v `apps/web/assets/` ako **manuálne udržiavané zdroje pravdy**. Pri zmene SVG: skopíruj kanonický kód z `branding-source/activity-logo.html` (sekcia *"08 SVG export"*).
- **`styles.css` a `theme.config.tsx`** — design tokens a Nextra config sa upravujú ručne podľa potreby.

**Ako to funguje (technicky):**

1. Stiahne fonty Albert Sans 700, Geist 400/500 z fontsource raw GitHub URL
2. Mergne `latin + latin-ext` subsety pomocou `fontTools` (slovenská diakritika)
3. PIL natívne nakreslí Chat Stack mark (9 tvarov: kruhy + zaoblené obdĺžniky) so 4× supersample anti-aliasingom
4. Vygeneruje OG image cez PIL ImageDraw + ImageFont
5. Skopíruje výsledky do `apps/docs/public/`

**Žiadny SVG renderer nie je potrebný** (`cairosvg` na macOS bez Homebrew zlyháva — používame natívny PIL prístup).

**Validácia:**

Skript vypisuje validáciu počtu znakov v Albert Sans 700 — má byť **368 znakov, missing diakritika: OK**. Ak by chýbali znaky `áéíóú` alebo `šč`, niečo je zle s mergom subsetov.

**Trvanie:** ~5-15 sekúnd (prvý beh stiahne fonty ~200KB, ďalšie behy idú z cache `/tmp/activity-brand-fonts/`).

### Súvisiace dokumenty

- **[Brand manuál](https://docs.activity.sportup.sk/ui/brand)** — kompletná špecifikácia
- **[ADR-013](https://docs.activity.sportup.sk/adr/0013-brand-v2)** — rozhodnutie prečo brand v2
- **[`branding-source/`](../branding-source/)** — interaktívne HTML zdroje brandu
