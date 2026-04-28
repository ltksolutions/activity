import React from 'react';
import { DocsThemeConfig } from 'nextra-theme-docs';

/**
 * Theme konfigurácia pre docs.activity.sportup.sk
 *
 * Branding (logo, accent farby) preberáme z Design manuálu pre sportup.sk.
 * Pri nasadení vlož finálne logo do /public/logo.svg a aktualizuj
 * primaryHue podľa branding farby.
 */
const config: DocsThemeConfig = {
  // Logo a brand
  logo: (
    <span style={{ fontWeight: 700, fontSize: '1.1rem' }}>
      <span style={{ color: 'var(--brand-color, currentColor)' }}>act</span>ivity
      <span style={{ marginLeft: '0.5rem', opacity: 0.6, fontWeight: 400, fontSize: '0.9rem' }}>
        docs
      </span>
    </span>
  ),
  logoLink: '/',

  // Project repo
  project: {
    link: 'https://github.com/ltksolutions/activity',
  },

  // Hlavička
  banner: {
    key: 'mvp-banner',
    text: 'Dokumentácia popisuje MVP fázu projektu. Niektoré features sú TBD.',
    dismissible: true,
  },

  // Navigácia v hlavičke
  navbar: {
    extraContent: null,
  },

  // Sidebar
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },

  // Footer
  footer: {
    text: (
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
        <span>
          © {new Date().getFullYear()} sportup. Open source pod{' '}
          <a href="https://github.com/ltksolutions/activity" target="_blank" rel="noopener">
            ltksolutions/activity
          </a>
        </span>
        <span style={{ opacity: 0.6 }}>
          Postavené na <a href="https://nextra.site" target="_blank" rel="noopener">Nextra</a>
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
    component: null, // null vypne search bar
  },

  // SEO a meta
  head: (
    <>
      <meta charSet="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Dokumentácia projektu activity — platforma pre slovenský šport" />
      <meta name="og:title" content="activity — dokumentácia" />
      <meta name="og:description" content="Verejná technická a produktová dokumentácia projektu activity" />
      <meta name="og:image" content="/og-image.png" />
      <meta name="theme-color" content="var(--brand-color, #0F6E56)" />
      <link rel="icon" href="/favicon.ico" />
    </>
  ),

  // Page title template
  useNextSeoProps() {
    return {
      titleTemplate: '%s — activity docs',
    };
  },

  // Dark mode
  darkMode: true,

  // Locale
  i18n: [
    { locale: 'sk', text: 'Slovenčina' },
  ],

  // Default lang for HTML
  primaryHue: {
    dark: 165,   // brand color hue v dark mode (zelený-tyrkysový)
    light: 165,  // brand color hue v light mode
  },
  primarySaturation: {
    dark: 60,
    light: 75,
  },

  // Toc
  toc: {
    backToTop: true,
    title: 'Na tejto stránke',
  },

  // Navigácia
  navigation: {
    prev: true,
    next: true,
  },

  // Color mode
  nextThemes: {
    defaultTheme: 'system',
  },

  // Misc
  gitTimestamp: ({ timestamp }) => (
    <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>
      Posledná aktualizácia: {timestamp.toLocaleDateString('sk-SK')}
    </span>
  ),
};

export default config;
