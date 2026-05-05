/*
 * SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
 * SPDX-License-Identifier: EUPL-1.2
 */
import React from 'react';
import { DocsThemeConfig } from 'nextra-theme-docs';

/**
 * Theme konfigurácia pre docs.activity.sportup.sk
 *
 * Brand v2: SK Blue (#1A3B8E) + SK Red (#C8243A), Chat Stack mark, Albert Sans + Geist.
 * Pozri ADR-013 (apps/docs/pages/adr/0013-brand-v2.mdx) a brand manuál (apps/docs/pages/ui/brand.mdx).
 */

/**
 * Logo komponent — inline SVG mark + HTML wordmark.
 *
 * Prečo inline SVG namiesto <img src="/logo.svg">:
 *  • SVG načítaný cez <img> nemá prístup k page fontom
 *    → <text font-family="Albert Sans"> sa renderuje system fallback-om
 *  • <img> nerešpektuje height={28} pri SVG s intrinsic viewBox → wordmark sa roztáhne
 *
 * Inline SVG (len Chat Stack mark) + HTML <span> wordmark:
 *  • Vidí Albert Sans z hlavnej stylesheety → typografia sedí s ostatnou stránkou
 *  • Predvídateľné rozmery (height/fontSize v px)
 *  • "docs" sufix vyzerá ako prirodzená časť wordmarku
 */
const Logo = () => (
  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
    {/* Chat Stack mark — viewBox 90×100 z brand manuálu, sekcia "08 SVG export" */}
    <svg
      viewBox="0 0 90 100"
      width={26}
      height={29}
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="activity"
      style={{ display: 'block', flexShrink: 0 }}
    >
      {/* Row 1: 1:1 */}
      <circle cx="14" cy="16" r="11" fill="#1A3B8E" />
      <circle cx="34" cy="16" r="11" fill="#1A3B8E" fillOpacity={0.38} />
      <rect x="50" y="9" width="26" height="15" rx="7.5" fill="#1A3B8E" fillOpacity={0.18} />
      {/* Row 2: group */}
      <circle cx="14" cy="50" r="11" fill="#1A3B8E" />
      <circle cx="30" cy="50" r="11" fill="#C8243A" fillOpacity={0.75} />
      <circle cx="46" cy="50" r="11" fill="#1A3B8E" fillOpacity={0.32} />
      <rect x="62" y="43" width="18" height="15" rx="7.5" fill="#C8243A" fillOpacity={0.18} />
      {/* Row 3: broadcast */}
      <circle cx="14" cy="84" r="11" fill="currentColor" fillOpacity={0.22} />
      <rect x="30" y="77" width="52" height="15" rx="7.5" fill="currentColor" fillOpacity={0.10} />
    </svg>

    {/* Wordmark "activity" — Albert Sans 700 cez page fonts */}
    <span
      style={{
        fontFamily: "'Albert Sans', ui-sans-serif, system-ui, sans-serif",
        fontWeight: 700,
        fontSize: 20,
        letterSpacing: '-0.02em',
        lineHeight: 1,
      }}
    >
      activity
    </span>

    {/* Sub-brand "docs" — utlmený, menší font */}
    <span
      style={{
        fontFamily: "'Geist', ui-sans-serif, system-ui, sans-serif",
        fontWeight: 500,
        fontSize: 13,
        opacity: 0.55,
        letterSpacing: '0.01em',
        lineHeight: 1,
      }}
    >
      docs
    </span>
  </span>
);

const config: DocsThemeConfig = {
  logo: <Logo />,
  logoLink: '/',

  // Project repo
  project: {
    link: 'https://github.com/ltksolutions/activity',
  },

  // Banner pre MVP
  banner: {
    key: 'mvp-banner',
    text: 'Dokumentácia popisuje MVP fázu projektu. Niektoré features sú TBD.',
    dismissible: true,
  },

  navbar: {
    extraContent: null,
  },

  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },

  // Footer
  footer: {
    text: (
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
        <span>
          © {new Date().getFullYear()} Ján Letko / LTK Solutions ·{' '}
          <a href="https://github.com/ltksolutions/activity/blob/main/LICENSE" target="_blank" rel="noopener">
            EUPL-1.2
          </a>{' '}
          (kód) ·{' '}
          <a href="https://github.com/ltksolutions/activity/blob/main/LICENSE-DOCS" target="_blank" rel="noopener">
            CC-BY-4.0
          </a>{' '}
          (docs) ·{' '}
          <a href="https://github.com/ltksolutions/activity" target="_blank" rel="noopener">
            ltksolutions/activity
          </a>
        </span>
        <span style={{ opacity: 0.6 }}>
          Klient projektu{' '}
          <a href="https://github.com/ltksolutions/sportup.sk" target="_blank" rel="noopener">
            sportup.sk
          </a>
        </span>
      </div>
    ),
  },

  // Edit page link
  editLink: {
    text: 'Upraviť túto stránku na GitHube →',
  },

  // Feedback link
  feedback: {
    content: 'Otázky? Otvor issue v repozitári →',
    labels: 'feedback',
  },

  // Search (zatiaľ vypnutý pre MVP)
  search: {
    placeholder: 'Vyhľadávanie zatiaľ nie je dostupné',
    component: null,
  },

  // SEO a meta
  head: (
    <>
      <meta charSet="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Dokumentácia projektu activity — platforma pre evidenciu aktivít, mentoring a komunikáciu v slovenskom športe" />

      {/* Favicon set */}
      <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
      <link rel="icon" type="image/x-icon" href="/favicon.ico" />
      <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
      <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
      <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />

      {/* PWA: web app manifest + installability */}
      <link rel="manifest" href="/site.webmanifest" />
      <meta name="application-name" content="activity docs" />
      <meta name="apple-mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-title" content="activity docs" />
      <meta name="apple-mobile-web-app-status-bar-style" content="default" />
      <meta name="mobile-web-app-capable" content="yes" />
      <meta name="format-detection" content="telephone=no" />

      {/* Open Graph */}
      <meta property="og:title" content="activity — dokumentácia" />
      <meta property="og:description" content="Verejná technická a produktová dokumentácia projektu activity" />
      <meta property="og:image" content="https://docs.activity.sportup.sk/og-image.png" />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:type" content="website" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:image" content="https://docs.activity.sportup.sk/og-image.png" />

      {/* Theme color (SK Blue light, INK dark) */}
      <meta name="theme-color" content="#1A3B8E" media="(prefers-color-scheme: light)" />
      <meta name="theme-color" content="#0E0E10" media="(prefers-color-scheme: dark)" />
      <meta name="color-scheme" content="light dark" />

      {/* Brand v2 fonty: Albert Sans (display) + Geist (body) + Geist Mono (code).
          Subset latin + latin-ext pre plnú slovenskú diakritiku. Pozri brand manuál §8. */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      <link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@700&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap&subset=latin,latin-ext"
      />
      <style>{`
        :root {
          --font-display: 'Albert Sans', ui-sans-serif, system-ui, sans-serif;
          --font-sans: 'Geist', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;
          --font-mono: 'Geist Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
        }
        body, .nextra-content {
          font-family: var(--font-sans);
        }
        .nextra-content h1, .nextra-content h2, .nextra-content h3,
        .nextra-content h4, .nextra-content h5, .nextra-content h6 {
          font-family: var(--font-display);
          letter-spacing: -0.02em;
        }
        code, pre, kbd, .nextra-code {
          font-family: var(--font-mono);
        }
      `}</style>
    </>
  ),

  useNextSeoProps() {
    return {
      titleTemplate: '%s — activity docs',
    };
  },

  // Dark mode podporované
  darkMode: true,

  i18n: [{ locale: 'sk', text: 'Slovenčina' }],

  /**
   * Brand v2 farby pre Nextra tému.
   *
   * Brand v2 má SK Blue ako primárnu farbu (#1A3B8E ≈ HSL(225, 70%, 33%))
   * a SK Red (#C8243A) ako akcent. V Nextra téme používame SK Blue ako
   * primaryHue — plní accent farby (linky, navigation, hover, headings).
   * SK Red sa aplikuje cez vlastné CSS overrides a tlačidlá, ak treba.
   */
  primaryHue: {
    dark: 225,   // SK Blue v dark mode
    light: 225,  // SK Blue v light mode
  },
  primarySaturation: {
    dark: 55,
    light: 70,
  },

  toc: {
    backToTop: true,
    title: 'Na tejto stránke',
  },

  navigation: {
    prev: true,
    next: true,
  },

  nextThemes: {
    defaultTheme: 'system',
  },

  gitTimestamp: ({ timestamp }) => (
    <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>
      Posledná aktualizácia: {timestamp.toLocaleDateString('sk-SK')}
    </span>
  ),
};

export default config;
