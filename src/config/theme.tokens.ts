export type ThemePalette = 'neon-blue' | 'cyan' | 'purple' | 'emerald';
export type GlowIntensity = 'low' | 'medium' | 'high';
export type LoaderStyle = 'pulse' | 'morphing-geometry' | 'scan';

export const ThemeTokens = {
  palettes: {
    'neon-blue': {
      '--color-primary': '#00F0FF',
      '--color-secondary': '#0055FF',
      '--color-bg-base': '#050505',
      '--color-text-base': '#E0E0E0',
      '--color-glow': 'rgba(0, 240, 255, 0.4)',
    },
    'cyan': {
      '--color-primary': '#00FFFF',
      '--color-secondary': '#008888',
      '--color-bg-base': '#020808',
      '--color-text-base': '#E0E0E0',
      '--color-glow': 'rgba(0, 255, 255, 0.4)',
    },
    'purple': {
      '--color-primary': '#B026FF',
      '--color-secondary': '#4D0099',
      '--color-bg-base': '#0A0010',
      '--color-text-base': '#E0E0E0',
      '--color-glow': 'rgba(176, 38, 255, 0.4)',
    },
    'emerald': {
      '--color-primary': '#00FF66',
      '--color-secondary': '#008033',
      '--color-bg-base': '#000A03',
      '--color-text-base': '#E0E0E0',
      '--color-glow': 'rgba(0, 255, 102, 0.4)',
    }
  }
};
