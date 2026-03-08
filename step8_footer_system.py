import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛑 M.A.C.DevOS Terminal Footer] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_footer_system():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    print_status("Engineering Global Footer System")

    # 1. Footer Component
    footer_content = """"use client";

import { Terminal, Github, Linkedin, Twitter, Mail } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative border-t border-foreground/10 bg-background/80 backdrop-blur-md pt-16 pb-8 px-6 lg:px-12 z-20">
      <div className="max-w-7xl mx-auto flex flex-col gap-12">
        
        {/* Top Section */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 md:gap-8">
          
          {/* Brand Identity */}
          <div className="md:col-span-5 flex flex-col gap-6">
            <div className="flex items-center gap-3 group">
              <div className="p-2 border border-primary/30 rounded-sm bg-primary/5">
                <Terminal className="w-5 h-5 text-primary" />
              </div>
              <span className="font-display font-bold text-xl tracking-widest text-foreground">
                M.A.C.<span className="text-primary">DevOS</span>
              </span>
            </div>
            <p className="font-sans text-sm text-foreground/50 leading-relaxed max-w-sm">
              Premium digital engineering and UI architecture. Deploying scalable, high-performance web infrastructure for the modern internet.
            </p>
            
            {/* System Status Indicator */}
            <div className="flex items-center gap-3 mt-2 w-fit px-3 py-1.5 border border-foreground/10 rounded-sm bg-foreground/[0.02]">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500 shadow-[0_0_10px_#10B981]"></span>
              </span>
              <span className="font-mono text-[10px] tracking-widest text-foreground/60 uppercase">All Systems Operational</span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="md:col-span-7 grid grid-cols-2 sm:grid-cols-3 gap-8">
            <div className="flex flex-col gap-4">
              <span className="font-mono text-xs tracking-widest text-foreground uppercase mb-2">Directory</span>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors">Architecture</a>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors">Deployments</a>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors">Protocols</a>
            </div>
            
            <div className="flex flex-col gap-4">
              <span className="font-mono text-xs tracking-widest text-foreground uppercase mb-2">Network</span>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors flex items-center gap-2">
                <Github className="w-4 h-4" /> GitHub
              </a>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors flex items-center gap-2">
                <Linkedin className="w-4 h-4" /> LinkedIn
              </a>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors flex items-center gap-2">
                <Twitter className="w-4 h-4" /> X / Twitter
              </a>
            </div>

            <div className="flex flex-col gap-4">
              <span className="font-mono text-xs tracking-widest text-foreground uppercase mb-2">Communicate</span>
              <a href="#" className="font-sans text-sm text-foreground/50 hover:text-primary transition-colors flex items-center gap-2">
                <Mail className="w-4 h-4" /> Initialize Link
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-foreground/5 gap-4">
          <p className="font-mono text-[10px] text-foreground/40 tracking-widest uppercase">
            © {currentYear} M.A.C.DevOS Engine. All rights reserved.
          </p>
          <div className="flex items-center gap-4">
            <span className="font-mono text-[10px] text-foreground/30 tracking-widest uppercase">V 1.0.0</span>
            <span className="w-1 h-1 bg-foreground/20 rounded-full"></span>
            <span className="font-mono text-[10px] text-foreground/30 tracking-widest uppercase">Next.js Edge</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
"""
    write_file("src/components/layout/Footer.tsx", footer_content)

    # 2. Update Layout to include Footer safely inside BootSequence
    layout_content = """import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import BootSequence from "@/components/layout/BootSequence";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import BackgroundFX from "@/components/ui/BackgroundFX";
import CustomCursor from "@/components/ui/CustomCursor";
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
      <body className="font-sans antialiased bg-background text-foreground selection:bg-primary selection:text-background relative">
        <BackgroundFX />
        <CustomCursor />
        <BootSequence>
          <Navbar />
          <div className="flex-grow">
            {children}
          </div>
          <Footer />
        </BootSequence>
      </body>
    </html>
  );
}
"""
    write_file("src/app/layout.tsx", layout_content)

    print_status("Global Footer integrated successfully")

if __name__ == "__main__":
    deploy_footer_system()