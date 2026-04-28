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
