"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Terminal, Github, Linkedin, Twitter } from 'lucide-react';

export default function Navbar() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    fetch('/api/admin/settings')
      .then(res => res.json())
      .then(data => setSettings(data));
  }, []);

  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-foreground/5">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="p-2 bg-primary/10 border border-primary/20 rounded group-hover:shadow-neon transition-all">
            <Terminal className="w-5 h-5 text-primary" />
          </div>
          <span className="font-display text-lg tracking-widest uppercase font-bold text-foreground">
            {settings?.siteName || "M.A.C.DevOS"}
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-8 font-mono text-[10px] tracking-[0.3em] uppercase text-foreground/50">
          <Link href="#architecture" className="hover:text-primary transition-colors">Architecture</Link>
          <Link href="#systems" className="hover:text-primary transition-colors">Systems</Link>
          <Link href="#deploy" className="hover:text-primary transition-colors">Deploy</Link>
          <div className="w-px h-4 bg-foreground/10 mx-2"></div>
          <div className="flex items-center gap-4">
            {settings?.githubUrl && <a href={settings.githubUrl} target="_blank" rel="noreferrer"><Github className="w-4 h-4 hover:text-primary transition-colors" /></a>}
            {settings?.linkedinUrl && <a href={settings.linkedinUrl} target="_blank" rel="noreferrer"><Linkedin className="w-4 h-4 hover:text-primary transition-colors" /></a>}
            {settings?.twitterUrl && <a href={settings.twitterUrl} target="_blank" rel="noreferrer"><Twitter className="w-4 h-4 hover:text-primary transition-colors" /></a>}
          </div>
        </div>
      </div>
    </nav>
  );
}
