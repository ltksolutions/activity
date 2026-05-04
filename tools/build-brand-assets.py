#!/usr/bin/env python3
"""
activity brand v2 — regen skript pre brand assety.

Generuje 19 PNG/ICO/manifest súborov + kópie do apps/docs/public/
zo zdrojov v branding-source/. Žiadne SVG dependency — Chat Stack
mark je 9 jednoduchých tvarov (kruhy + zaoblené obdĺžniky), PIL ich
kreslí natívne s anti-aliasingom (4× supersample).

Pre OG image stiahne fonty z fontsource (latin + latin-ext mergnuté
cez fontTools — kompletná slovenská diakritika).

Použitie:
    python3 tools/build-brand-assets.py

Závislosti:
    /usr/bin/python3 (built-in macOS Python 3.9+)
    Pillow         — pip install --user Pillow
    fonttools      — pip install --user fonttools brotli

Output:
    apps/web/assets/    (19 súborov: logá PNG, favicon set, OG image, ICO)
    apps/web/favicon.ico    (root, legacy)
    apps/docs/public/   (kópie 11 brand assetov)

Pozri ADR-013 (apps/docs/pages/adr/0013-brand-v2.mdx) pre kontext.
Pozri brand manuál (apps/docs/pages/ui/brand.mdx) pre špecifikáciu.
"""
import os, sys, urllib.request, ssl, shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print('ERROR: Pillow nie je nainštalovaný. Spusti:')
    print('  pip install --user Pillow')
    sys.exit(1)

try:
    from fontTools.ttLib import TTFont
    from fontTools.merge import Merger
except ImportError:
    print('ERROR: fontTools nie je nainštalovaný. Spusti:')
    print('  pip install --user fonttools brotli')
    sys.exit(1)


# ─── Cesty ────────────────────────────────────────────────────────────
REPO    = Path(__file__).resolve().parent.parent
WEB     = REPO / 'apps/web/assets'
WEBROOT = REPO / 'apps/web'
DOCS    = REPO / 'apps/docs/public'
FONTS   = Path('/tmp/activity-brand-fonts')
FONTS.mkdir(exist_ok=True)


# ─── Brand tokens (zo source: branding-source/activity-brand-manual.html) ──
SK_BLUE       = (0x1A, 0x3B, 0x8E)
SK_BLUE_LIGHT = (0x4A, 0x6D, 0xC4)   # dark mode variant
SK_RED        = (0xC8, 0x24, 0x3A)
SK_RED_LIGHT  = (0xD9, 0x4A, 0x5E)   # dark mode variant
INK           = (0x0E, 0x0E, 0x10)
PAPER         = (0xFA, 0xFA, 0xF7)


def rgba(rgb, alpha=1.0):
    return (rgb[0], rgb[1], rgb[2], int(round(alpha * 255)))


# ═════════════════════════════════════════════════════════════════════
# Fonty: stiahnutie z fontsource + merge latin + latin-ext
# ═════════════════════════════════════════════════════════════════════

def fetch_font(url, dest):
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    print(f'  fetch {dest.name}')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        dest.write_bytes(r.read())
    return dest


def merge_subsets(woff_a, woff_b, out_ttf):
    """Merge latin + latin-ext woff subsets do jedneho TTF (pre PIL)."""
    if out_ttf.exists():
        return out_ttf
    tmp_ttfs = []
    for w in (woff_a, woff_b):
        f = TTFont(str(w))
        f.flavor = None
        t = w.with_suffix('.ttf')
        f.save(str(t))
        tmp_ttfs.append(str(t))
    merged = Merger().merge(tmp_ttfs)
    merged.save(str(out_ttf))
    return out_ttf


def setup_fonts():
    """Stiahni a merge fonty pre OG image rendering."""
    base_url = 'https://raw.githubusercontent.com/fontsource/font-files/main/fonts/google'
    fonts = {
        'AlbertSans-Bold': (
            f'{base_url}/albert-sans/files/albert-sans-latin-700-normal.woff',
            f'{base_url}/albert-sans/files/albert-sans-latin-ext-700-normal.woff',
        ),
        'Geist-Medium': (
            f'{base_url}/geist/files/geist-latin-500-normal.woff',
            f'{base_url}/geist/files/geist-latin-ext-500-normal.woff',
        ),
        'Geist-Regular': (
            f'{base_url}/geist/files/geist-latin-400-normal.woff',
            f'{base_url}/geist/files/geist-latin-ext-400-normal.woff',
        ),
    }
    result = {}
    for name, (url_latin, url_ext) in fonts.items():
        latin = fetch_font(url_latin, FONTS / f'{name}-latin.woff')
        ext   = fetch_font(url_ext,   FONTS / f'{name}-latinext.woff')
        result[name] = merge_subsets(latin, ext, FONTS / f'{name}-merged.ttf')
    return result


# ═════════════════════════════════════════════════════════════════════
# Chat Stack mark renderer (PIL natívne, žiadny SVG)
# ═════════════════════════════════════════════════════════════════════
# Source viewBox: 90×100 (z brand manuálu, sekcia 08 SVG export):
#   Row 1 (1:1):       circles cx=14,34 r=11 + pill x=50 y=9 w=26 h=15 rx=7.5
#   Row 2 (group):     circles cx=14,30,46 r=11 + pill x=62 y=43 w=18 h=15 rx=7.5
#   Row 3 (broadcast): circle cx=14 r=11 + pill x=30 y=77 w=52 h=15 rx=7.5

PALETTE_LIGHT = {'blue': SK_BLUE, 'red': SK_RED, 'muted': INK}
PALETTE_WHITE = {'blue': PAPER, 'red': PAPER, 'muted': PAPER,
                 'b38': 0.40, 'b18': 0.22, 'r75': 0.65,
                 'r18': 0.20, 'b32': 0.32, 'm22': 0.20, 'm10': 0.12}


def render_mark(size, palette=PALETTE_LIGHT, padding_pct=0.06,
                bg=None, rounded_radius=None):
    """Render Chat Stack mark do square `size` × `size` PNG s padding."""
    SS = 4  # supersample faktor pre kvalitu
    big = size * SS
    canvas = Image.new('RGBA', (big, big), (0, 0, 0, 0))

    if bg is not None:
        bg_layer = Image.new('RGBA', (big, big), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bg_layer)
        if rounded_radius:
            bd.rounded_rectangle([0, 0, big, big],
                                 radius=rounded_radius * SS,
                                 fill=bg + (255,))
        else:
            bd.rectangle([0, 0, big, big], fill=bg + (255,))
        canvas.alpha_composite(bg_layer)

    # Mark má viewBox 90×100, fit do (size - 2*padding)
    avail = size * (1 - 2 * padding_pct)
    vb_w, vb_h = 90, 100
    scale = min(avail / vb_w, avail / vb_h) * SS
    eff_w = vb_w * scale
    eff_h = vb_h * scale
    off_x = (big - eff_w) / 2
    off_y = (big - eff_h) / 2

    d = ImageDraw.Draw(canvas)
    p = palette

    def circ(cx, cy, r, color, op):
        x0 = off_x + (cx - r) * scale
        y0 = off_y + (cy - r) * scale
        x1 = off_x + (cx + r) * scale
        y1 = off_y + (cy + r) * scale
        d.ellipse([x0, y0, x1, y1], fill=rgba(color, op))

    def pill(x, y, ww, hh, rx, color, op):
        x0 = off_x + x * scale
        y0 = off_y + y * scale
        x1 = off_x + (x + ww) * scale
        y1 = off_y + (y + hh) * scale
        d.rounded_rectangle([x0, y0, x1, y1], radius=rx * scale, fill=rgba(color, op))

    # Row 1: 1:1
    circ(14, 16, 11, p['blue'], 1.0)
    circ(34, 16, 11, p['blue'], p.get('b38', 0.38))
    pill(50, 9, 26, 15, 7.5, p['blue'], p.get('b18', 0.18))
    # Row 2: group
    circ(14, 50, 11, p['blue'], 1.0)
    circ(30, 50, 11, p['red'],  p.get('r75', 0.75))
    circ(46, 50, 11, p['blue'], p.get('b32', 0.32))
    pill(62, 43, 18, 15, 7.5, p['red'], p.get('r18', 0.18))
    # Row 3: broadcast
    circ(14, 84, 11, p['muted'], p.get('m22', 0.22))
    pill(30, 77, 52, 15, 7.5, p['muted'], p.get('m10', 0.10))

    # Downsample z 4× supersample
    return canvas.resize((size, size), Image.LANCZOS)


# ═════════════════════════════════════════════════════════════════════
# Build pipeline
# ═════════════════════════════════════════════════════════════════════

def build():
    print('═══ activity brand v2 — regen ═══')
    print(f'Repo: {REPO}')
    print(f'Web:  {WEB}')
    print(f'Docs: {DOCS}')

    # 0. Validácia
    if not WEB.exists():
        print(f'ERROR: {WEB} neexistuje. Si v správnom repe?')
        sys.exit(1)

    print('\n[fonty]')
    fonts = setup_fonts()

    # Validácia diakritiky
    f = TTFont(str(fonts['AlbertSans-Bold']))
    cmap = f.getBestCmap()
    test = 'aščťžáéíóúýňľôä'
    miss = [c for c in test if ord(c) not in cmap]
    print(f'  Albert Sans 700: {len(cmap)} znakov, missing diakritika: {miss or "OK"}')

    # 1. Mark only PNGs
    print('\n[mark only PNGs]')
    for s in (256, 512, 1024):
        img = render_mark(s, PALETTE_LIGHT, padding_pct=0.05)
        p = WEB / f'logo-mark-{s}.png'
        img.save(p, optimize=True)
        print(f'  ✓ {p.name}  {p.stat().st_size // 1024}K')

    # 2. Favicons (mark only, transparent)
    print('\n[favicon PNGs]')
    for s in (16, 32, 192, 512):
        img = render_mark(s, PALETTE_LIGHT, padding_pct=0.06)
        p = WEB / f'favicon-{s}x{s}.png'
        img.save(p, optimize=True)
        print(f'  ✓ {p.name}  {p.stat().st_size // 1024 or 1}K')

    # 3. Apple touch icon (paper bg, 180×180)
    print('\n[apple touch icon]')
    img = render_mark(180, PALETTE_LIGHT, padding_pct=0.18, bg=PAPER)
    p = WEB / 'apple-touch-icon.png'
    img.save(p, optimize=True)
    print(f'  ✓ {p.name}  {p.stat().st_size // 1024}K')

    # 4. Maskable (Android adaptive — 20% safe area, biely mark, SK Blue bg)
    print('\n[maskable icons]')
    for s in (192, 512):
        img = render_mark(s, PALETTE_WHITE, padding_pct=0.20, bg=SK_BLUE)
        p = WEB / f'icon-maskable-{s}.png'
        img.save(p, optimize=True)
        print(f'  ✓ {p.name}  {p.stat().st_size // 1024}K')

    # 5. favicon.ico (multi-res 16/32/48)
    print('\n[favicon.ico]')
    ico_imgs = [render_mark(s, PALETTE_LIGHT, padding_pct=0.06) for s in (16, 32, 48)]
    ico_path = WEB / 'favicon.ico'
    ico_imgs[0].save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print(f'  ✓ assets/favicon.ico  {ico_path.stat().st_size} bytes')
    # Aj root favicon.ico (legacy odkazy)
    ico_imgs[0].save(WEBROOT / 'favicon.ico', format='ICO',
                     sizes=[(16, 16), (32, 32), (48, 48)])
    print(f'  ✓ web/favicon.ico (root)')

    # 6. OG image 1200×630
    print('\n[OG image]')
    OG_W, OG_H = 1200, 630
    canvas = Image.new('RGB', (OG_W, OG_H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # Top tricolor band (12px)
    strip_h = 12
    draw.rectangle([0, 0, OG_W // 3, strip_h], fill=(255, 255, 255))
    draw.rectangle([OG_W // 3, 0, 2 * OG_W // 3, strip_h], fill=SK_BLUE)
    draw.rectangle([2 * OG_W // 3, 0, OG_W, strip_h], fill=SK_RED)

    # Mark vľavo
    mark_size = 360
    mark_img = render_mark(mark_size, PALETTE_LIGHT, padding_pct=0.0)
    mark_x = 100
    mark_y = (OG_H - mark_size) // 2
    canvas.paste(mark_img, (mark_x, mark_y), mark_img)

    # Wordmark Albert Sans 700
    font_word = ImageFont.truetype(str(fonts['AlbertSans-Bold']),  168)
    font_tag  = ImageFont.truetype(str(fonts['Geist-Medium']),      36)
    font_subt = ImageFont.truetype(str(fonts['Geist-Regular']),     28)
    font_url  = ImageFont.truetype(str(fonts['Geist-Medium']),      22)

    text_x = mark_x + mark_size + 30
    word_y = OG_H // 2 - 130
    draw.text((text_x, word_y), 'activity', fill=INK, font=font_word)

    tag_y = word_y + 200
    draw.text((text_x, tag_y), 'komunikačná platforma pre šport',
              fill=(0x3A, 0x3A, 0x3E), font=font_tag)

    sub_y = tag_y + 60
    draw.text((text_x, sub_y), '1:1  ·  skupiny  ·  broadcast',
              fill=SK_BLUE, font=font_subt)

    url_text = 'activity.sportup.sk'
    ubox = draw.textbbox((0, 0), url_text, font=font_url)
    uw = ubox[2] - ubox[0]
    draw.text((OG_W - uw - 60, OG_H - 50), url_text,
              fill=(0x6B, 0x6B, 0x70), font=font_url)

    # Bottom red border
    draw.rectangle([0, OG_H - strip_h, OG_W, OG_H], fill=SK_RED)

    og_path = WEB / 'og-image.png'
    canvas.save(og_path, optimize=True, quality=92)
    print(f'  ✓ og-image.png  {og_path.stat().st_size // 1024}K')

    # 7. Kópie do apps/docs/public/
    print('\n[copy to apps/docs/public]')
    docs_assets = [
        'favicon.ico', 'favicon.svg',
        'favicon-16x16.png', 'favicon-32x32.png',
        'favicon-192x192.png', 'favicon-512x512.png',
        'icon-maskable-192.png', 'icon-maskable-512.png',
        'apple-touch-icon.png', 'og-image.png',
        'logo.svg', 'logo-dark.svg', 'logo-mark.svg',
    ]
    for fn in docs_assets:
        src = WEB / fn
        dst = DOCS / fn
        if src.exists():
            shutil.copy(src, dst)
            print(f'  ✓ docs/public/{fn}')
        else:
            print(f'  ⚠ skip {fn} (zdroj neexistuje)')

    print('\n══════════════════════════════════════════')
    print('HOTOVO — všetky brand assety regenerované.')
    print('══════════════════════════════════════════')
    print('\nPozn.: SVG súbory v apps/web/assets/ sa NEgenerujú týmto skriptom.')
    print('Sú zdrojom pravdy a editujú sa ručne podľa branding-source/activity-logo.html')
    print('(sekcia "08 SVG export").')


if __name__ == '__main__':
    build()
