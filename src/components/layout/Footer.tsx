"use client";
import { useState, useEffect } from 'react';
import { Terminal, Github, Linkedin, Twitter, Instagram, Youtube, Globe, Mail } from 'lucide-react';

const ICON_MAP: any = {
  github: Github,
  linkedin: Linkedin,
  twitter: Twitter,
  instagram: Instagram,
  youtube: Youtube,
  website: Globe
};

export default function Footer() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    fetch('/api/admin/settings').then(res => res.json()).then(data => setSettings(data));
  }, []);

  return (
    <footer className="w-full py-20 px-6 border-t border-foreground/5 bg-background z-20">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="md:col-span-2 flex flex-col gap-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-5 h-5 text-primary" />
            <span className="font-display uppercase font-bold text-foreground">{settings?.siteName || "M.A.C.DevOS"}</span>
          </div>
          <p className="text-foreground/50 text-sm max-w-sm">Premium digital engineering and UI architecture.</p>
          <div className="flex items-center gap-2 px-3 py-1 border border-emerald-500/20 bg-emerald-500/5 text-emerald-500 w-max rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-mono text-[9px] uppercase tracking-widest">All Systems Operational</span>
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Social Matrix</h4>
          <div className="flex flex-col gap-4">
            {settings?.socialLinks?.map((link: any, i: number) => {
              const Icon = ICON_MAP[link.platform] || Globe;
              return (
                <a key={i} href={link.url} target="_blank" className="flex items-center gap-2 font-mono text-xs text-foreground/60 hover:text-primary transition-all">
                  <Icon className="w-4 h-4" /> {link.platform.toUpperCase()}
                </a>
              );
            })}
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Communicate</h4>
          <a href={`mailto:${settings?.contactEmail || 'macdevos53@gmail.com'}`} className="flex items-center gap-2 font-mono text-xs text-foreground/60 hover:text-primary transition-all">
            <Mail className="w-4 h-4" /> {settings?.contactEmail || "Initialize Link"}
          </a>
        </div>
      </div>
    </footer>
  );
}
