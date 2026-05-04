import React from 'react';
import { DocsThemeConfig } from 'nextra-theme-docs';

/**
 * Theme konfigurácia pre docs.activity.sportup.sk
 *
 * Brand: navy + red (slovenská národná farebnosť)
 * Founded on sportup.sk Design Manual v2.0 · 2026
 */
const config: DocsThemeConfig = {
  // Logo — SVG image z /public
  logo: (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <img src="/logo.svg" alt="activity" height={28} style={{ display: 'block' }} />
      <span
        style={{
          marginLeft: '0.25rem',
          opacity: 0.5,
          fontWeight: 400,
          fontSize: '0.85rem',
        }}
      >
        docs
      </span>
    </div>
  ),
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
          © {new Date().getFullYear()} activity. Open source pod{' '}
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
