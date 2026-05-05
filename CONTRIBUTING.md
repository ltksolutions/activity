<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
# Contributing to activity

Vďaka za záujem prispieť. Tento dokument popisuje **ako prispievať** do projektu — či už ide o opravu preklepu v dokumentácii, alebo nový backend feature.

Repozitár je **monorepo** s viacerými aplikáciami. Tento dokument pokrýva najmä **prácu s dokumentáciou** (`apps/docs`), ktorá je momentálne hlavná aktívna časť projektu. Pre kontribúciu do iných apps (až vzniknú) pribudnú samostatné `CONTRIBUTING.md` v ich priečinkoch.

## Obsah

- [Princípy](#princípy)
- [Editácia dokumentácie](#editácia-dokumentácie)
- [Pridanie nového dokumentu](#pridanie-nového-dokumentu)
- [Pridanie novej sekcie](#pridanie-novej-sekcie)
- [Štýl písania](#štýl-písania)
- [Markdown a MDX konvencie](#markdown-a-mdx-konvencie)
- [Linky medzi dokumentami](#linky-medzi-dokumentami)
- [Lokálny preview](#lokálny-preview)
- [Pull requesty](#pull-requesty)
- [Ownership a review](#ownership-a-review)

## Princípy

### Dokumentácia je živý dokument

Nečakaj, kým bude *"hotová"*. Ak vidíš nepresnosť, nečitateľnú vetu, alebo chýbajúce info — oprav. Otvor PR. Niekto ho posúdi.

### Jeden zdroj pravdy

Dokumentácia žije **iba v `apps/docs/pages/`** ako MDX súbory. Žiadne duplicity v iných miestach repozitára.

### Slovenčina ako primárny jazyk

MVP je v slovenčine. Pri pridávaní obsahu **nepoužívaj angličtinu** (okrem technických termínov, ktoré nemajú slovenský ekvivalent — napr. *commit*, *deployment*, *throughput*).

V budúcnosti pridáme paralel v EN/CS — to bude nová iterácia, nie teraz.

### Dokument musí byť **čítateľný samostatne**

Predpokladaj, že čitateľ dokumentu nečítal predošlé. Pridaj kontext, prepojenia, glossary linky.

## Editácia dokumentácie

### Najjednoduchší spôsob — priamo na GitHube

Pre **drobné opravy** (preklep, doplnenie odseku, oprava linku):

1. Otvor súbor v GitHub UI: `apps/docs/pages/<priečinok>/<súbor>.mdx`
2. Klikni na ikonu ceruzky (Edit this file)
3. Uprav
4. Dole *"Commit changes"* → *"Create a new branch and start a pull request"*
5. Daj PR popisný názov: `docs: oprava sekcie X v Y`
6. Submitni

Vercel automaticky vytvorí preview deployment — uvidíš, ako bude dokument vyzerať.

### Pre väčšie zmeny — lokálne

Pre **väčšie úpravy** (nový dokument, refaktoring sekcie, viac súborov naraz):

```bash
git clone <repo-url>
cd activity
npm install
git checkout -b docs/<popis-zmeny>
npm run dev:docs
```

Editor MDX súborov: VS Code odporúčaný, s rozšírením *MDX* od unifiedjs.

Po úpravách:

```bash
git add apps/docs/
git commit -m "docs: <popis zmeny>"
git push origin docs/<popis-zmeny>
```

Otvor PR cez GitHub UI.

## Pridanie nového dokumentu

### 1. Premysli si, kam patrí

Štruktúra dokumentácie je založená na **vrstvách**:

| Sekcia | Obsahuje | Kedy sem pridávať |
|---|---|---|
| Root (`pages/*.mdx`) | Top-level kostra (overview, architecture, ...) | Veľmi zriedka — iba ak ide o úplne novú top-level tému |
| `pages/features/` | Špecifické moduly (mentoring, courier, ...) | Nový subsystém, ktorý je tematicky uzavretý |
| `pages/workflows/` | Per kategória používateľa | Nová kategória používateľov |
| `pages/acl/` | ACL matice | Nová matica oprávnení (zriedka) |
| `pages/ops/` | Prevádzka | Operačné aspekty (monitoring, security, atď.) |
| `pages/ui/` | UI a dizajn | Dizajnové princípy, mockupy |

Pre väčšinu prípadov ide o `features/`, `workflows/` alebo `ops/`.

### 2. Vytvor MDX súbor

```
apps/docs/pages/<priečinok>/<názov-bez-pripony>.mdx
```

Konvencia mena súboru: **kebab-case**, výstižný, bez diakritiky.

Príklad: `apps/docs/pages/features/incident-management.mdx`

### 3. Štruktúra dokumentu

Použi nasledujúcu šablónu:

```markdown
# Názov dokumentu

Krátky úvodný odsek (1–3 vety) — čo tento dokument popisuje, pre koho je užitočný.

## Doménový kontext

Vysvetli **prečo** táto vec existuje, aký problém rieši. Bez kontextu sú technické detaily ťažko stráviteľné.

## Hlavné koncepty

Rozpíš kľúčové koncepty a entity.

## Životný cyklus / Workflow

Ako sa to používa krok za krokom.

## ACL / Bezpečnosť

Ak je relevantné — kto má aké práva.

## Implementačné body

Praktické info pre vývojárov.

## Otvorené otázky

Veci, ktoré sú TBD.

## Nasleduje

Linky na súvisiace dokumenty.
```

Nie každá sekcia je povinná — vyber, čo dáva zmysel.

### 4. Aktualizuj `_meta.json` v priečinku

V tom istom priečinku otvor `_meta.json` a pridaj záznam:

```json
{
  "existing-doc": "Existujúci dokument",
  "incident-management": "Správa incidentov"
}
```

Hodnota je **zobrazované meno** v navigácii. Kľúč zodpovedá názvu súboru bez prípony.

**Poradie v JSON-e určuje poradie v navigácii.** Daj nový dokument tam, kam logicky patrí (nie automaticky na koniec).

### 5. Aktualizuj `glossary.mdx`

Ak tvoj nový dokument zavádza **nové pojmy alebo skratky**, pridaj ich do `apps/docs/pages/glossary.mdx`. To zabezpečí, že nové pojmy sú dohľadateľné.

### 6. Otvor PR

```bash
git add apps/docs/pages/
git commit -m "docs: pridať dokument o správe incidentov"
git push origin docs/incident-management
```

PR template ti pomôže vyplniť potrebné info.

## Pridanie novej sekcie

Pre úplne nový **priečinok** (napr. `pages/integrations/`):

1. Vytvor priečinok `apps/docs/pages/<nazov-sekcie>/`
2. Vytvor `_meta.json` v ňom:
   ```json
   {
     "first-doc": "Prvý dokument"
   }
   ```
3. Pridaj prvý dokument
4. Otvor `apps/docs/pages/_meta.json` a pridaj sekciu:
   ```json
   {
     "...": "...",
     "ui": "UI",
     "integrations": "Integrácie",  ← nová sekcia
     "glossary": "Slovník pojmov"
   }
   ```

Nová sekcia sa objaví v hlavnom menu Nextra.

## Štýl písania

### Píš pre čitateľa, nie pre seba

- **Konkrétne, krátke vety**. Žiadne *"Z hľadiska implementácie je možné konštatovať, že..."*. Skús *"Implementačne to vyzerá takto:"*.
- **Aktívny rod**. *"Mentor zaznamená sedenie"*, nie *"Sedenie je zaznamenávané mentorom"*.
- **Konkrétne príklady**. Po abstraktnom popise daj reálnu situáciu: *"Napríklad mentor Peter Novák..."*

### Štruktúra

- **Hierarchické nadpisy** — `#`, `##`, `###` v logickom poradí
- **Krátke odseky** — max 4–5 viet
- **Tabuľky** pre porovnávacie info (ACL matice, mapping atribútov, ...)
- **Bulletové zoznamy** ak položky nemajú vnútornú logiku (kde záleží len na tom, že existujú)
- **Číslované zoznamy** ak ide o postupnosť krokov

### Vyhni sa

- **Marketingovému jazyku** — *"revolúcia"*, *"jedinečný"*, *"ultimátny"*. Toto je technická dokumentácia.
- **Vag fráz** — *"v niektorých prípadoch môže byť..."*. Buď konkrétny: *"keď sa stane X, systém robí Y"*.
- **Duplicite** — ak je niečo v inom dokumente, **odkáž** sa. Neopisuj.

### Tone

Konzervatívny, neformálny ale presný. Predstav si, že to píšeš kolegovi, ktorý je inteligentný, ale nemá kontext tohto projektu.

## Markdown a MDX konvencie

### Code bloky

```markdown
\`\`\`typescript
const x: number = 5;
\`\`\`
```

Vždy uvedz jazyk pre syntax highlighting (`typescript`, `javascript`, `bash`, `json`, `yaml`, `mongodb`).

### Inline kód

`` `Person.firstName` `` pre identifikátory, názvy súborov, krátke kódové fragmenty.

### Citáty

```markdown
> *"Zložité veci sa dajú vysvetliť jednoducho."*
```

Citáty len pre skutočné citáty alebo dôležité poznámky.

### Tabuľky

```markdown
| Stĺpec 1 | Stĺpec 2 |
|---|---|
| hodnota | hodnota |
```

Bez nadbytočných formátovacích trikov.

### Emojis a ikony

Striedmo. Sú užitočné pre:
- ✓ označenie hotových položiek
- ⚠️ varovania
- 🔒 citlivé časti
- 📋 zoznamy

Nepoužívaj emojis na ozdobu alebo pre fun. Toto je technická dokumentácia.

### MDX rozšírenia

V MDX sa dá vkladať **React komponenty**:

```mdx
import { Callout } from 'nextra/components';

<Callout type="warning">
Pozor — toto je dôležité.
</Callout>
```

Dostupné komponenty: `Callout`, `Cards`, `Tabs`, `Steps` a ďalšie z [Nextra](https://nextra.site/docs/guide/built-ins).

**Nevytváraj vlastné komponenty** bez konzultácie s tímom — udržujeme dokumentáciu jednoduchú.

## Linky medzi dokumentami

Toto je dôležité, lebo Nextra používa **iné formáty** než klasické markdown.

### Pravidlá

**Linky bez `.mdx` prípony**:

```mdx
✓ [Mentoring](/features/mentoring)
✗ [Mentoring](/features/mentoring.mdx)
✗ [Mentoring](features/mentoring.md)
```

**Absolútne cesty od root-u** (začínajú `/`):

```mdx
✓ [Architektúra](/architecture)
✓ [ACL pre Courier](/acl/matrix-courier)
```

**Relatívne v rovnakom priečinku** — žiadny prefix:

```mdx
V súbore apps/docs/pages/features/mentoring.mdx:

✓ [Courier](courier)
✓ [Komentáre](activity-comments)
```

**Linky na sekciu vnútri dokumentu**:

```mdx
✓ [pozri ACL](/features/mentoring#acl)
```

**Externé linky** — normálne:

```mdx
✓ [GitHub](https://github.com/ltksolutions/activity)
```

### Anchor text

Text linku má byť **popisný**, nie generický:

```mdx
✗ Pre detaily [klikni sem](/features/mentoring).
✓ Pre detaily pozri [Mentoring](/features/mentoring).
```

## Lokálny preview

### Spustenie

Z root-u monorepa:

```bash
npm run dev:docs
```

Otvor [http://localhost:3000](http://localhost:3000). Hot-reload funguje — uložením súboru sa stránka obnoví.

### Build pred PR

Pred submit-nutím PR-u skontroluj, že **build prebehne bez errorov**:

```bash
npm run build:docs
```

Vercel preview deployment sa vytvorí automaticky pri PR-e, takže výsledok uvidíš aj v cloude. Ale lokálny build je rýchlejší pre kontrolu.

### Časté chyby

| Symptóm | Príčina |
|---|---|
| `Module not found: <súbor>` | Link na neexistujúci súbor — skontroluj cestu |
| Stránka chýba v navigácii | Nie je v `_meta.json` v príslušnom priečinku |
| `Hydration error` | MDX má neuzavreté JSX tagy alebo chybnú syntax |
| Tabuľka sa zle renderuje | Chýbajúce `|` na začiatku/konci, alebo zlý počet stĺpcov |

## Pull requesty

### PR template

Pri otvorení PR-u uvidíš template — vyplň ho:

- **Čo a prečo** — krátky popis zmeny
- **Typ zmeny** — bug fix / new content / refactor / formatting
- **Súvisiace issues** — odkazy ak existujú
- **Checklist** — pred submit-nutím

### Branch naming

```
docs/<popis-zmeny>      # pre zmeny v apps/docs
fix/<popis-fixu>        # pre opravy
feat/<popis-feature>    # pre nové features
chore/<popis>           # pre údržbu (deps update, atď.)
```

### Commit messages

Konvencia podľa [Conventional Commits](https://www.conventionalcommits.org/):

```
docs: pridať dokument o správe incidentov
docs: oprava preklepov v courier.mdx
docs: refaktor sekcie ACL v mentoring.mdx
fix: oprava broken linku v glossary
chore: update Nextra na 2.14
```

### Veľkosť PR

Preferujeme **menšie PR-y** — ľahšie na review, rýchlejší merge.

- Ak meníš jeden dokument → jeden PR
- Ak refaktoruješ celú sekciu → môže byť väčší, ale rozdel na logické kroky

### Review proces

- Každý PR potrebuje **aspoň 1 schválenie** od ownera danej sekcie (pozri `.github/CODEOWNERS`)
- Po schválení autor PR-u (alebo owner) merge-uje
- Squash merge je default (jeden pekný commit per PR)

## Ownership a review

### CODEOWNERS

V `.github/CODEOWNERS` je mapa **kto je zodpovedný za ktorú sekciu**:

```
# Mentoring + Courier features
/apps/docs/pages/features/mentoring.mdx    @<owner>
/apps/docs/pages/features/courier.mdx      @<owner>

# Workflows
/apps/docs/pages/workflows/                @<owner>
```

Pri PR-e GitHub **automaticky tagne** ownerov ako reviewerov.

### Becoming an owner

Ak pravidelne prispievaš do nejakej sekcie, môžeš sa stať jej co-ownerom. Otvor issue s návrhom a tím to schváli.

## Otázky

Niečo nie je jasné? Niečo chýba?

- **Otázky o procese** → otvor GitHub Discussion s tagom `meta`
- **Bug v dokumentácii** → GitHub Issue s tagom `docs:bug`
- **Návrh nového dokumentu** → GitHub Issue s tagom `docs:feature`
- **Diskusia o obsahu** → GitHub Discussion s tagom `docs:content`

## Licenčný model a SPDX

Projekt používa **dual licenčný model** — každá kontribúcia musí byť kompatibilná:

| Časť projektu | Licencia | Pokrytie |
|---|---|---|
| Zdrojový kód (TS/TSX/CSS/JS/Python) | **EUPL-1.2** | `apps/*/src`, packages, build tools |
| Dokumentácia, brand, marketing | **CC-BY-4.0** | `apps/docs/`, `apps/web/`, `branding-source/`, `*.md` |

Projekt je [REUSE-compliant](https://reuse.software/spec/) — každý nový súbor musí obsahovať SPDX header (alebo byť pokrytý v `REUSE.toml`).

### SPDX hlavičky pre nové súbory

**Zdrojový kód** (TS/TSX/CSS/JS/MJS):
```ts
/*
 * SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
 * SPDX-License-Identifier: EUPL-1.2
 */
```

**Dokumentácia** (MD):
```md
<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
```

> **MDX súbory** (`apps/docs/pages/**/*.mdx`) **nemajú inline header** — MDX parser nepodporuje HTML kommentáre. Ich licencia (CC-BY-4.0) je pokrytá cez `REUSE.toml`. Nové MDX súbory v `apps/docs/pages/` a podadresároch automaticky dedia tento aggregate header — nič nežiadať pri ich tvorbe.

**Python** (build tools):
```python
#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
# SPDX-License-Identifier: EUPL-1.2
```

**HTML** (marketing web):
```html
<!DOCTYPE html>
<!--
SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
SPDX-License-Identifier: CC-BY-4.0
-->
```

Ak si nový k REUSE, použi automatický skript, ktorý headery pridá správne podľa typu súboru:

```bash
python3 tools/add-spdx-headers.py --apply    # pridá všetky chýbajúce
python3 tools/add-spdx-headers.py --check    # exit 1 ak niečo chýba
```

### Verifikácia

Lokálne pred PR-om:
```bash
pip install reuse
reuse lint        # musí ukázať "Congratulations! Your project is compliant with version 3.3 of the REUSE Specification"
```

### Copyright pre nových prispievateľov

Keď pridávaš významnú kontribúciu, môžeš pridať svoj copyright riadok navrch existujúceho:

```ts
/*
 * SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
 * SPDX-FileCopyrightText: 2026 Tvoje Meno <tvoj@email.com>
 * SPDX-License-Identifier: EUPL-1.2
 */
```

Tým sa zachová úplná atribúcia bez nutnosti CLA.

---

## Vďaka

Každá kontribúcia, aj malá, posúva projekt vpred. Vďaka, že sa zapájaš.
