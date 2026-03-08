"use client";

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
