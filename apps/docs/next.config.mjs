/*
 * SPDX-FileCopyrightText: 2026 Ján Letko <activity@ltk.solutions>
 * SPDX-License-Identifier: EUPL-1.2
 */
import nextra from 'nextra';

const withNextra = nextra({
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.tsx',
  defaultShowCopyCode: true,
});

export default withNextra({
  reactStrictMode: true,
  trailingSlash: false,
  // Pre statické nasadenie na Vercel:
  // output: 'export',  // odkomentuj pre static export
});
