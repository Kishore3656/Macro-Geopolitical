import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#0f172a',
        },
        panel: '#0a0b0f',
        surface: '#13151d',
        amber: '#ffb867',
        danger: '#ff2d2d',
        success: '#6ecf8a',
        cyan: '#00ffff',
      },
      animation: {
        spin: 'spin 1s linear infinite',
      },
    },
  },
  plugins: [],
};

export default config;
