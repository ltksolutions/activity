# Public assets

Tento priečinok obsahuje **statické assety** servované Nextrom — logá, ikony, OG image-y.

## Pri inicializácii projektu sem doplň:

| Súbor | Účel | Formát | Veľkosť |
|---|---|---|---|
| `logo.svg` | Hlavné logo v hlavičke | SVG | ~32px výška |
| `logo-dark.svg` | Logo pre dark mode (voliteľné) | SVG | ~32px výška |
| `favicon.ico` | Browser tab ikona | ICO | 16x16, 32x32 multi-res |
| `favicon-32x32.png` | Fallback favicon | PNG | 32x32 |
| `apple-touch-icon.png` | iOS home screen ikona | PNG | 180x180 |
| `og-image.png` | Open Graph náhľad pri zdieľaní | PNG | 1200x630 |

Branding assety sa preberajú z **Design manuálu pre sportup.sk** projekt. Pri implementácii konzultuj s tímom dizajnu.

## Ako sa používajú

Assety sa servírujú z root-u domény:

- `logo.svg` → `https://docs.activity.sportup.sk/logo.svg`
- `favicon.ico` → `https://docs.activity.sportup.sk/favicon.ico`

V `theme.config.tsx` na ne odkazujeme cez absolútne cesty:

```tsx
logo: <img src="/logo.svg" alt="activity" height={32} />
```

V meta tagoch (`<head>` v `theme.config.tsx`):

```tsx
<link rel="icon" href="/favicon.ico" />
<meta name="og:image" content="/og-image.png" />
```

Po pridaní reálnych assetov môžeš tento README zmazať.
