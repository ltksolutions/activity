#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
# SPDX-License-Identifier: EUPL-1.2
"""
Pridá SPDX headery do všetkých textových zdrojových súborov v repe.

Idempotentný — keď súbor už má SPDX header, preskočí ho.
Rešpektuje shebangy (#!/usr/bin/env python3), XML/HTML doctype,
React 'use client' direktívy, atď. — header pridá za ne.

Spustenie:
    python3 tools/add-spdx-headers.py            # dry-run + summary
    python3 tools/add-spdx-headers.py --apply    # skutočne zmení súbory
    python3 tools/add-spdx-headers.py --check    # exit 1 ak chýbajú headery

Pozri ADR-014 a REUSE Specification 3.3:
    https://reuse.software/spec/
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

COPYRIGHT = "2026 Ján Letko <activity@ltk.solutions>"
LICENSE_CODE = "EUPL-1.2"
LICENSE_DOCS = "CC-BY-4.0"


# ─── Klasifikácia súborov ─────────────────────────────────────────────────
# Pravidlá pre to, akú licenciu dostane súbor podľa cesty + extension.
# Predpoklad: každý súbor je BUĎ "code" (EUPL-1.2) ALEBO "docs" (CC-BY-4.0).

def classify(rel_path: Path) -> str | None:
    """Vráti 'EUPL-1.2', 'CC-BY-4.0' alebo None (preskoč)."""
    s = rel_path.as_posix()
    name = rel_path.name
    ext = rel_path.suffix.lower()

    # Skip — je v REUSE.toml alebo nemá zmysel pridávať header
    if any(s.startswith(prefix) for prefix in [
        '.git/', 'node_modules/', '.next/', 'dist/', 'build/', 'coverage/',
        '.vercel/', '.turbo/', 'LICENSES/',
    ]):
        return None
    if name in ('LICENSE', 'LICENSE-DOCS', 'REUSE.toml', '.DS_Store',
                'CITATION.cff', 'package.json', 'package-lock.json',
                'site.webmanifest', '.gitignore', '.gitattributes',
                '.editorconfig', '.npmrc'):
        return None
    if ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico',
               '.woff', '.woff2', '.ttf', '.otf', '.eot',
               '.lock', '.tsbuildinfo'):
        return None
    if ext == '.json':
        return None  # JSON nemá comment syntax → REUSE.toml

    # Branding source → docs
    if s.startswith('branding-source/'):
        return None  # spracované cez REUSE.toml

    # SVG v assets/ → docs (brand asset)
    if ext == '.svg' and ('/assets/' in s or '/public/' in s):
        return None  # spracované cez REUSE.toml (brand assets)

    # Markdown/MDX → docs
    if ext in ('.md', '.mdx'):
        return LICENSE_DOCS

    # Marketing web HTML → docs (content)
    if s.startswith('apps/web/') and ext == '.html':
        return LICENSE_DOCS

    # Marketing web partials → docs
    if 'apps/web/partials/' in s:
        return LICENSE_DOCS

    # Source code → EUPL-1.2
    if ext in ('.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
               '.css', '.scss', '.sass',
               '.py', '.sh', '.bash',
               '.yml', '.yaml', '.toml',
               '.html'):  # default HTML mimo apps/web
        return LICENSE_CODE

    return None


# ─── Comment štýly per extension ──────────────────────────────────────────

def comment_style(ext: str, name: str) -> tuple[str, str, str]:
    """Vráti (prefix, line_prefix, suffix) pre comment block."""
    if ext in ('.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.css', '.scss', '.sass'):
        return ('/*\n', ' * ', '\n */\n')
    if ext in ('.py', '.sh', '.bash', '.yml', '.yaml', '.toml') or name.startswith('.') or 'Dockerfile' in name:
        return ('', '# ', '\n')
    if ext in ('.md', '.mdx', '.html', '.svg', '.xml'):
        return ('<!--\n', '', '\n-->\n')
    return ('', '# ', '\n')


def make_header(license_id: str, ext: str, name: str) -> str:
    """Vytvorí kompletný SPDX header pre daný súbor."""
    prefix, line_prefix, suffix = comment_style(ext, name)
    if line_prefix:
        line1 = f'{line_prefix}SPDX-FileCopyrightText: {COPYRIGHT}'
        line2 = f'{line_prefix}SPDX-License-Identifier: {license_id}'
        return f'{prefix}{line1}\n{line2}{suffix}'
    else:  # HTML/MD/SVG comment block
        return f'{prefix}SPDX-FileCopyrightText: {COPYRIGHT}\nSPDX-License-Identifier: {license_id}{suffix}'


# ─── Detekcia, kde vložiť header (po shebang, doctype, atď.) ──────────────

def find_insert_position(content: str, ext: str) -> int:
    """Vráti byte offset, kam vložiť header. 0 = na začiatok."""
    if not content:
        return 0

    # Shebang #!/...
    if content.startswith('#!'):
        nl = content.find('\n')
        if nl != -1:
            return nl + 1

    # XML declaration <?xml ...?>
    if content.startswith('<?xml'):
        end = content.find('?>')
        if end != -1:
            nl = content.find('\n', end)
            return (nl + 1) if nl != -1 else (end + 2)

    # HTML doctype
    if content.lstrip().lower().startswith('<!doctype'):
        nl = content.find('\n')
        if nl != -1:
            return nl + 1

    # MDX import statements / 'use client' / 'use strict' direktívy
    # → vložiť pred ne
    return 0


# ─── Detekcia existujúceho SPDX header-a (idempotency) ────────────────────

SPDX_RE = re.compile(r'SPDX-FileCopyrightText:|SPDX-License-Identifier:', re.I)

def has_spdx(content: str) -> bool:
    """Skontroluje, či súbor už má SPDX header (v prvých 1500 bajtoch)."""
    return bool(SPDX_RE.search(content[:1500]))


# ─── Hlavná logika ────────────────────────────────────────────────────────

def iter_files() -> list[Path]:
    """Vráti všetky kandidátske súbory v repe (rešpektuje .gitignore-like)."""
    skip_dirs = {
        '.git', 'node_modules', '.next', 'dist', 'build', 'coverage',
        '.vercel', '.turbo', 'LICENSES', '.cache',
    }
    files = []
    for p in REPO.rglob('*'):
        if not p.is_file():
            continue
        if any(d in p.parts for d in skip_dirs):
            continue
        files.append(p)
    return files


def process(apply: bool, check_only: bool) -> int:
    """Pridá / skontroluje headery. Vráti exit code."""
    added = 0
    skipped_have = 0
    skipped_other = 0
    missing = []
    by_license = {LICENSE_CODE: 0, LICENSE_DOCS: 0}

    for path in iter_files():
        rel = path.relative_to(REPO)
        license_id = classify(rel)
        if license_id is None:
            skipped_other += 1
            continue

        try:
            content = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, IsADirectoryError):
            skipped_other += 1
            continue

        if has_spdx(content):
            skipped_have += 1
            continue

        if check_only:
            missing.append(rel.as_posix())
            continue

        header = make_header(license_id, rel.suffix.lower(), rel.name)
        pos = find_insert_position(content, rel.suffix.lower())
        new_content = content[:pos] + header + content[pos:]

        if apply:
            path.write_text(new_content, encoding='utf-8')
        added += 1
        by_license[license_id] += 1
        if not apply:
            print(f'  + {rel.as_posix():60s}  [{license_id}]')

    print()
    print('═══ SUMMARY ═══')
    print(f'  total files scanned:  {added + skipped_have + skipped_other}')
    print(f'  already has SPDX:     {skipped_have}')
    print(f'  skipped (binary/etc): {skipped_other}')
    print(f'  {"applied" if apply else ("missing" if check_only else "would add")}: {added}')
    print(f'    EUPL-1.2:           {by_license[LICENSE_CODE]}')
    print(f'    CC-BY-4.0:          {by_license[LICENSE_DOCS]}')

    if check_only and missing:
        print()
        print('Missing SPDX headers:')
        for m in missing:
            print(f'  - {m}')
        return 1

    return 0


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    check = '--check' in sys.argv
    sys.exit(process(apply=apply, check_only=check))
