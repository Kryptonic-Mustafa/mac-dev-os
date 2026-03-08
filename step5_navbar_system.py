import os
import time
from pathlib import Path

# --- Configuration ---
PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🌐 M.A.C.DevOS Network Hub] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_navbar_system():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found. Ensure you are inside the 'mac-dev-os' directory.")
        return

    print_status("Engineering Global Navigation & Theme Controller")

    # 1. Navbar Component
    navbar_content = """"use client";

import { useState, useEffect } from 'react';
import { useVisualSettings } from '@/lib/storage/visualStorage';
import { ThemePalette } from '@/config/theme.tokens';
import { Terminal, Palette } from 'lucide-react';

export default function Navbar() {
  const { palette, updatePalette, isMounted } = useVisualSettings();
  const [scrolled, setScrolled] = useState(false);

  // Glassmorphic scroll effect
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Prevent hydration mismatch
  if (!isMounted) return <div className="h-20 w-full fixed top-0 bg-transparent z-50"></div>;

  const themes: { id: ThemePalette; label: string; color: string }[] = [
    { id: 'neon-blue', label: 'Neon Blue', color: '#00F0FF' },
    { id: 'cyan', label: 'Cyan', color: '#00FFFF' },
    { id: 'purple', label: 'Purple', color: '#B026FF' },
    { id: 'emerald', label: 'Emerald', color: '#00FF66' },
  ];

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 border-b ${
        scrolled 
          ? 'bg-background/80 backdrop-blur-md border-primary/20 py-4 shadow-[0_4px_30px_rgba(0,0,0,0.5)]' 
          : 'bg-transparent border-transparent py-6'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-12 flex items-center justify-between">
        
        {/* Brand Identity */}
        <div className="flex items-center gap-3 group cursor-pointer">
          <div className="p-2 border border-primary/30 rounded-sm bg-primary/5 group-hover:bg-primary/10 transition-colors">
            <Terminal className="w-5 h-5 text-primary" />
          </div>
          <span className="font-display font-bold text-xl tracking-widest text-foreground">
            M.A.C.<span className="text-primary transition-colors duration-300">DevOS</span>
          </span>
        </div>

        {/* Navigation & Theme Toggles */}
        <div className="flex items-center gap-8">
          
          <nav className="hidden md:flex items-center gap-8 font-mono text-xs tracking-[0.15em] text-foreground/60">
            <a href="#" className="hover:text-primary transition-colors">ARCHITECTURE</a>
            <a href="#" className="hover:text-primary transition-colors">SYSTEMS</a>
            <a href="#" className="hover:text-primary transition-colors">DEPLOY</a>
          </nav>

          {/* Dynamic Theme Controller */}
          <div className="flex items-center gap-4 pl-8 border-l border-foreground/10">
            <Palette className="w-4 h-4 text-foreground/40" />
            <div className="flex items-center gap-3">
              {themes.map((t) => (
                <button
                  key={t.id}
                  onClick={() => updatePalette(t.id)}
                  className={`w-4 h-4 rounded-full border border-foreground/20 transition-all duration-300 hover:scale-125 ${
                    palette === t.id 
                      ? 'scale-125 shadow-[0_0_12px_var(--color-primary)] border-primary' 
                      : 'opacity-50 hover:opacity-100'
                  }`}
                  style={{ backgroundColor: t.color }}
                  title={`Switch to ${t.label} protocol`}
                  aria-label={`Switch to ${t.label} theme`}
                />
              ))}
            </div>
          </div>
          
        </div>
      </div>
    </header>
  );
}
"""
    write_file("src/components/layout/Navbar.tsx", navbar_content)

    # 2. Update Root Layout to inject Navbar
    layout_content = """import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import BootSequence from "@/components/layout/BootSequence";
import Navbar from "@/components/layout/Navbar";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space-grotesk" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains-mono" });

export const metadata: Metadata = {
  title: "M.A.C.DevOS | Premium Digital Engineering",
  description: "Advanced full-stack engineering and UI systems architecture.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased bg-background text-foreground selection:bg-primary selection:text-background">
        <BootSequence>
          <Navbar />
          {children}
        </BootSequence>
      </body>
    </html>
  );
}
"""
    write_file("src/app/layout.tsx", layout_content)

    print_status("Global Navigation & Theme Hub deployed successfully")

if __name__ == "__main__":
    deploy_navbar_system()