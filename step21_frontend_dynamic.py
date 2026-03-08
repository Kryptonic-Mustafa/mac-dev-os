import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🌐 M.A.C.DevOS Frontend] {message}...")
    time.sleep(0.5)

def deploy_dynamic_frontend():
    # ---------------------------------------------------------
    # 1. DYNAMIC NAVBAR INTEGRATION
    # ---------------------------------------------------------
    print_status("Synchronizing Navbar with Master Settings")
    navbar_path = PROJECT_PATH / "src/components/layout/Navbar.tsx"
    
    navbar_content = """"use client";

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
"""
    with open(navbar_path, "w", encoding="utf-8") as f:
        f.write(navbar_content)

    # ---------------------------------------------------------
    # 2. DYNAMIC PROJECTS (DEPLOYMENT MATRIX)
    # ---------------------------------------------------------
    print_status("Injecting Live Deployment Matrix into Portfolio")
    projects_path = PROJECT_PATH / "src/components/sections/Projects.tsx"
    
    projects_content = """"use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Github, ExternalLink, Cpu } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function DeploymentMatrix() {
  const [projects, setProjects] = useState<any[]>([]);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    fetch('/api/admin/projects')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setProjects(data);
      });
  }, []);

  useGSAP(() => {
    if (projects.length === 0) return;
    
    gsap.from(".project-card", {
      y: 100,
      opacity: 0,
      duration: 1,
      stagger: 0.2,
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });
  }, [projects]);

  return (
    <section id="deploy" ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        <div className="mb-20">
          <div className="flex items-center gap-3 mb-4">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Active Deployments</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">System Matrix</h2>
        </div>

        <div className="grid grid-cols-1 gap-12">
          {projects.map((proj) => (
            <div key={proj.id} className="project-card flex flex-col md:flex-row gap-12 group">
              <div className="w-full md:w-1/3 flex flex-col gap-6">
                <div className="flex items-center gap-4 text-primary/40 font-mono text-[10px] tracking-widest uppercase">
                  <Cpu className="w-4 h-4" /> {proj.systemId}
                </div>
                <div className="flex flex-wrap gap-2">
                  {proj.tech.split(',').map((t: string) => (
                    <span key={t} className="px-3 py-1 border border-primary/20 bg-primary/5 text-primary font-mono text-[9px] uppercase tracking-widest">
                      {t.trim()}
                    </span>
                  ))}
                </div>
              </div>

              <div className="w-full md:w-2/3 border-l border-foreground/10 pl-0 md:pl-12">
                <h3 className="text-2xl md:text-3xl font-display text-foreground group-hover:text-primary transition-colors mb-4">{proj.title}</h3>
                <p className="text-foreground/60 font-sans leading-relaxed mb-8 max-w-2xl">{proj.description}</p>
                <div className="flex items-center gap-8">
                  {proj.repoLink && (
                    <a href={proj.repoLink} target="_blank" className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-foreground/40 hover:text-primary transition-colors">
                      <Github className="w-4 h-4" /> Repository
                    </a>
                  )}
                  {proj.liveLink && (
                    <a href={proj.liveLink} target="_blank" className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-primary hover:text-primary/70 transition-colors">
                      <ExternalLink className="w-4 h-4" /> Live Instance
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
          {projects.length === 0 && (
             <div className="font-mono text-sm text-foreground/30 uppercase tracking-widest py-10">No assets currently live in matrix.</div>
          )}
        </div>
      </div>
    </section>
  );
}
"""
    with open(projects_path, "w", encoding="utf-8") as f:
        f.write(projects_content)

    # ---------------------------------------------------------
    # 3. PUBLIC GET API FOR SETTINGS
    # ---------------------------------------------------------
    print_status("Establishing Public Read-Only API Route for Settings")
    api_settings_path = PROJECT_PATH / "src/app/api/admin/settings/route.ts"
    
    api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  const settings = await db.systemSettings.findUnique({ where: { id: 'master_config' } });
  return NextResponse.json(settings || { siteName: "M.A.C.DevOS" });
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const settings = await db.systemSettings.upsert({
      where: { id: 'master_config' },
      update: data,
      create: { id: 'master_config', ...data }
    });
    return NextResponse.json(settings);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to save settings' }, { status: 500 });
  }
}
"""
    with open(api_settings_path, "w", encoding="utf-8") as f:
        f.write(api_content)

    print_status("Frontend synchronization complete.")

if __name__ == "__main__":
    deploy_dynamic_frontend()