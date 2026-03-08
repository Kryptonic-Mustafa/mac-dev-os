import os
import time
from pathlib import Path

# --- Configuration ---
# Since your terminal is already inside the 'mac-dev-os' folder, we use the current working directory.
PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🎨 M.A.C.DevOS UI Engine] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    # Ensure directory exists just in case
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Injected: {filepath}")

def deploy_visual_system():
    # Verify we are in the Next.js project root by checking for package.json
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found. Please make sure your terminal is inside the 'mac-dev-os' directory.")
        return

    print_status("Initializing Master Visual Settings System")

    # 1. Theme Tokens System
    theme_tokens_content = """export type ThemePalette = 'neon-blue' | 'cyan' | 'purple' | 'emerald';
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
"""
    write_file("src/config/theme.tokens.ts", theme_tokens_content)

    # 2. Tailwind Configuration Bridge
    tailwind_config_content = """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--color-bg-base)",
        foreground: "var(--color-text-base)",
        primary: "var(--color-primary)",
        secondary: "var(--color-secondary)",
        glow: "var(--color-glow)",
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        display: ['var(--font-space-grotesk)', 'sans-serif'],
        mono: ['var(--font-jetbrains-mono)', 'monospace'],
      },
      boxShadow: {
        'neon': '0 0 20px var(--color-glow), 0 0 40px var(--color-glow)',
      }
    },
  },
  plugins: [],
};
export default config;
"""
    write_file("tailwind.config.ts", tailwind_config_content)

    # 3. Hydration-Safe Local Storage Hook
    visual_storage_content = """"use client";

import { useState, useEffect } from 'react';
import { ThemeTokens, ThemePalette, LoaderStyle } from '@/config/theme.tokens';
import { VisualConfig } from '@/config/visual.config';

export function useVisualSettings() {
  const [isMounted, setIsMounted] = useState(false);
  const [palette, setPalette] = useState<ThemePalette>(VisualConfig.defaultPalette as ThemePalette);
  const [loaderStyle, setLoaderStyle] = useState<LoaderStyle>(VisualConfig.loaderStyle as LoaderStyle);

  // Hydrate from localStorage safely on client mount
  useEffect(() => {
    setIsMounted(true);
    const savedPalette = (localStorage.getItem('macdevos-palette') as ThemePalette) || VisualConfig.defaultPalette;
    const savedLoader = (localStorage.getItem('macdevos-loader') as LoaderStyle) || VisualConfig.loaderStyle;
    
    setPalette(savedPalette);
    setLoaderStyle(savedLoader);
    applyThemeToDOM(savedPalette);
  }, []);

  // DOM Injection Engine
  const applyThemeToDOM = (activePalette: ThemePalette) => {
    const tokens = ThemeTokens.palettes[activePalette];
    const root = document.documentElement;
    
    Object.entries(tokens).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  };

  const updatePalette = (newPalette: ThemePalette) => {
    setPalette(newPalette);
    localStorage.setItem('macdevos-palette', newPalette);
    applyThemeToDOM(newPalette);
  };

  const updateLoaderStyle = (newLoader: LoaderStyle) => {
    setLoaderStyle(newLoader);
    localStorage.setItem('macdevos-loader', newLoader);
  };

  return { isMounted, palette, loaderStyle, updatePalette, updateLoaderStyle };
}
"""
    write_file("src/lib/storage/visualStorage.ts", visual_storage_content)

    # 4. Global CSS (Overwriting default Next.js globals)
    globals_css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  /* Fallback to Neon Blue on SSR before JS injects custom tokens */
  --color-primary: #00F0FF;
  --color-secondary: #0055FF;
  --color-bg-base: #050505;
  --color-text-base: #E0E0E0;
  --color-glow: rgba(0, 240, 255, 0.4);
}

body {
  background-color: var(--color-bg-base);
  color: var(--color-text-base);
  overflow-x: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

/* Premium OS Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: var(--color-bg-base);
}
::-webkit-scrollbar-thumb {
  background: var(--color-secondary);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--color-primary);
}
"""
    write_file("src/app/globals.css", globals_css_content)

    print_status("Visual System successfully integrated into M.A.C.DevOS")

if __name__ == "__main__":
    deploy_visual_system()